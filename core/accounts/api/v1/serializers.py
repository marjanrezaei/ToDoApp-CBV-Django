from rest_framework import serializers
from ...models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

 
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length = 255, write_only=True)


    class Meta:
        model = User
        fields = ['email', 'password', 'password1']
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError("Passwords does not match")
        
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return super().validate(attrs)
        
    def create(self, validated_data):
        validated_data.pop('password1', None) # remove password1 from validated_data
        return User.objects.create_user(**validated_data) # create_user is a method in the User model that creates a user with the given email and password
    


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    override the default AuthTokenSerializer to use email instead of username
    """
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                msg = _('User is not verified.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            msg = _('User is not verified.')
            raise serializers.ValidationError(msg, code='authorization')
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    """
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        return super().validate(attrs)
 
    
class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer to manage extra user info
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "description",
        ]
        
        
class ResendActivationSerializer(serializers.Serializer):
    """
    Serializer for resending activation email.
    """
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        if user_obj.is_verified:
            raise serializers.ValidationError("User is already verified.")

        attrs['user'] = user_obj
        return super().validate(attrs)
    

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting password.
    """
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        attrs['user'] = user_obj
        return super().validate(attrs)
    
    
class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for resetting password.
    """
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError("Passwords does not match")
        
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        
        return super().validate(attrs)
    
