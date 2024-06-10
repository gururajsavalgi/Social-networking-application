from django.contrib import admin  # noqa: F401
from django.urls import path
from SocialApp import views  # noqa: F401
from django.conf import settings
from django.conf.urls.static import static
from .views import FriendsList, LoginView,UserListView, SendFriendRequestView, AcceptFriendRequestView,ListFriendRequestsView,UserRegistrationView,DeclineFriendRequestView

urlpatterns = [
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
