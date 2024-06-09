
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate,login
from django.http import JsonResponse
import random
from django.db.models import Q
from django.db.models import Case, When
#from .models import User
from itertools import chain
from django.contrib.auth import get_user_model
# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import FriendRequest, Friendship
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest
from .serializers import FriendRequestSerializer, FriendshipSerializer
#my chages
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer,AcceptFriendRequestSerializer,FriendRequestSerializer,UserRegistrationSerializer,LoginSerializer
from rest_framework import status,generics,permissions
from rest_framework.decorators import api_view
from django.db import IntegrityError, transaction
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
# Create your views here.




class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'A user with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'Success':'Logged In'
        })

class LoginView1(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data,{'Successfully': 'Logged in'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def index(request):
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="GET":
      return render(request,"login.html")

    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            # A backend authenticated the credentials
            print("hi")
            login(request,user)
            messages.success(request, "You have logged in successfully!")
            return redirect('index')
        else:
            print("bye")
            return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect("/login")
def sign(request):
    if request.method=="GET":
      return render(request,"sign.html")
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1!=password2:
            return HttpResponse("incorrect password")
        else:
            my_user=User.objects.create_user(username,email,password1)
            my_user.save()
            return redirect('login')
    
def user(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'user.html', {'users': users})





class FriendsListt(generics.ListAPIView):
    print("tkkkk")
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(user1=user)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'email']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Exclude the current user from the queryset
        return User.objects.exclude(id=self.request.user.id)
class SendFriendRequestView(APIView):
    def post(self, request, to_user_id):
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if not can_send_friend_request(request.user):
            return Response({"error": "You can only send 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Friend request already sent."}, status=status.HTTP_200_OK)
    
class SendFriendRequestVie(APIView):
    def post(self, request, user_id):
        print("hiiiiiiiii2")
        to_user = User.objects.get(id=user_id)
        from_user = request.user
        try:
            with transaction.atomic():
              friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

            if created:
                return Response({"data": "Friend request sent sucessfully"},status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:   
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
          return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
User = get_user_model()

@login_required
def accept_friend_request(request, request_id):
    print("hi")
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        Friendship.objects.get_or_create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()
    return redirect('list_friend_requests')

@login_required
def list_friend_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'friend_requests.html', {'received_requests': received_requests})

class ListFriendRequestsView(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user)
    

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('list_friend_requests')

class DeclineFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
       friend_request = get_object_or_404(FriendRequest, id=request_id)
       if friend_request.to_user == request.user:
        friend_request.delete()
       return Response({"detail": "Deleted"},status=status.HTTP_204_NO_CONTENT)

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_user == request.user:
          Friendship.objects.get_or_create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()
        return Response({"detail": "ACCEPTED"},status=status.HTTP_204_NO_CONTENT)
        # return redirect('list_friend_requests')
        
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"detail": "Friend request not found or not authorized to accept"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AcceptFriendRequestSerializer(friend_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetFriendRequestVie(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = Friendship.get_friends(request.user)
        serializer_class = FriendshipSerializer
        return Response(friends,status=status.HTTP_204_NO_CONTENT)
        # return redirect('list_friend_requests')

class FriendsListt(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        friends = Friendship.objects.filter(request.user)
        return Response(friends,status=status.HTTP_204_NO_CONTENT)

class FriendsList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        friends = Friendship.get_friends(request.user)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def can_send_friend_request(from_user):
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    recent_requests_count = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
    return recent_requests_count < 3