
from django.contrib import messages  # noqa: F401
from django.shortcuts import render, HttpResponse, redirect  # noqa: F401
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate,login  # noqa: F401
from django.http import JsonResponse  # noqa: F401
import random  # noqa: F401
from django.db.models import Q# noqa: F401
from django.db.models import Case, When# noqa: F401
#from .models import User
from itertools import chain# noqa: F401
from django.contrib.auth import get_user_model
# myapp/views.py
from django.shortcuts import get_object_or_404
from .models import FriendRequest, Friendship
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest  # noqa: F811
from .serializers import FriendRequestSerializer, FriendshipSerializer# noqa: F401
#my change
from rest_framework.generics import ListAPIView# noqa: F401
from django.contrib.auth.models import User # noqa: F401, F811
from .serializers import UserSerializer,AcceptFriendRequestSerializer,FriendRequestSerializer,UserRegistrationSerializer,LoginSerializer  # noqa: F811
from rest_framework import status,generics,permissions
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
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



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
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

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'email']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Exclude the current user from the queryset
        return User.objects.exclude(id=self.request.user.id)
class SendFriendRequestView(APIView):
    authentication_classes = [SessionAuthentication]
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
    
User = get_user_model()

    
def can_send_friend_request(from_user):
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    recent_requests_count = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
    return recent_requests_count < 3

class ListFriendRequestsView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user)
    

class DeclineFriendRequestView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
       friend_request = get_object_or_404(FriendRequest, id=request_id)
       if friend_request.to_user == request.user:
        friend_request.delete()
       return Response({"detail": "Friend request Deleted"},status=status.HTTP_204_NO_CONTENT)

class AcceptFriendRequestView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_user == request.user:
          Friendship.objects.get_or_create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()
        return Response({"detail": "Friend request ACCEPTED"},status=status.HTTP_204_NO_CONTENT)
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

class FriendsList(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        friends = Friendship.get_friends(request.user)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    