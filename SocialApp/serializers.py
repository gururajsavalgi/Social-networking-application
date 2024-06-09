from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    def validate_email(self, value):
        if not serializers.EmailField().run_validation(value):
            raise serializers.ValidationError("Wrong email format.")
        return value
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp']


class AcceptFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id']

    def save(self):
        friend_request = self.instance
        user1 = friend_request.from_user
        user2 = friend_request.to_user

        Friendship.objects.create(user1=user1, user2=user2)
        Friendship.objects.create(user1=user2, user2=user1)

        friend_request.delete()


class FriendshipSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta:
        model = Friendship
        fields = ['id', 'user1', 'user2']


class FriendRequestSerializer(serializers.ModelSerializer):  # noqa: F811
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp']
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email').lower() 
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")
            
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid email or password.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data