from django.contrib import admin
from django.urls import path
from SocialApp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import  FriendsList, LoginView, accept_friend_request,list_friend_requests, decline_friend_request,UserListView, SendFriendRequestView, AcceptFriendRequestView,ListFriendRequestsView,UserRegistrationView,login_view,DeclineFriendRequestView

urlpatterns = [
    #path("", views.index, name='index'),
    #path("user/", views.user, name='user'),
    #path("login/",views.loginUser,name="login"),
   # path("logout/",views.logoutuser,name="logout"),
    #path("sign_in/",views.sign,name="sign"),
    #path('send_friend_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    #path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    #path('friend_requests/', list_friend_requests, name='list_friend_requests'),
    #path('decline_friend_request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    #path('api/accepted_friend_requests/', AcceptedFriendRequestsView.as_view(), name='accepted_friend_requests'),
    path('api/users/', UserListView.as_view(), name='user-list-api'),
    path('api/send-friend-request/<int:to_user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('api/friend-requests/', ListFriendRequestsView.as_view(), name='list-friend-requests'),
    path('api/accept-friend-request/<int:request_id>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('api/decline-friend-request/<int:request_id>/', DeclineFriendRequestView.as_view(), name='decline-friend-request'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('friends/', FriendsList.as_view(), name='friends-list'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
