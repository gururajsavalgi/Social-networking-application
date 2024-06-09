from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model


# Create your models here.
class Sign_in(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password1=models.CharField(max_length=50)

class login(models.Model):
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)

# myapp/models.py



User = get_user_model()  # noqa: F811

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2','timestamp')

    def get_friends(user):
         user_ids = list(Friendship.objects.filter(user1=user).values_list('user2', flat=True)) + \
                    list(Friendship.objects.filter(user2=user).values_list('user1', flat=True))
         return User.objects.filter(id__in=user_ids)