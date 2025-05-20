from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import  TokenObtainPairView
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from .utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings



class RegistrationApiView(generics.GenericAPIView):
    """
    API view to register a new user.
    """
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data ={
                "email": email,
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_time_limited_token_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'marjan@gmail.com', to=[email])
            EmailThread(email_obj).start()
         
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  
    def get_time_limited_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom view to handle token authentication.
    """  
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        

class CustomDiscardAuthToken(APIView):
    """
    Custom view to handle token discard.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle JWT token authentication.
    """
    serializer_class = CustomTokenObtainPairSerializer
   
    

class ChangePasswordApiView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    API view to change password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'details': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
class ProfileApiView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update user profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
    

class TestEmailSend(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        self.email = 'rezaei.marjann@gmail.com'
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_time_limited_token_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'marjan@gmail.com', to=[self.email])
        EmailThread(email_obj).start()
        
        return Response("test email sent")
    
    def get_time_limited_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
        
        
class ActivationApiView(APIView):
    """
    API view to activate user account.
    """   
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({"error": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST) 
        user_obj = User.objects.get(id=user_id)
        if user_obj.is_verified:
            return Response({"error": "Account already activated"}, status=status.HTTP_400_BAD_REQUEST)     
        user_obj.is_verified = True
        user_obj.save()
        
        return Response({"success": "Account activated successfully"}, status=status.HTTP_200_OK)
    
    
    
class ResendActivationApiView(generics.GenericAPIView):
    """
    API view to resend activation email.
    """
    serializer_class = ResendActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_time_limited_token_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'marjan@gmail.com', to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({"success": "Activation email resent"}, status=status.HTTP_200_OK)

    def get_time_limited_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordApiView(generics.GenericAPIView):
    """
    API view to reset password.
    """
    serializer_class = ResetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_time_limited_token_for_user(user_obj)
        email_obj = EmailMessage('email/reset_password_email.tpl', {'token': token}, 'marjan@gmail.com', to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({"success": "Reset password email sent"}, status=status.HTTP_200_OK)

    def get_time_limited_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        # This is a JWT access token, valid for a short time (default 5 minutes)
        return str(refresh.access_token)


class ResetPasswordConfirmApiView(generics.GenericAPIView):
    """
    API view to confirm reset password.
    """
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({"error": "Reset password link expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({"error": "Invalid reset password link"}, status=status.HTTP_400_BAD_REQUEST) 
        user_obj = User.objects.get(id=user_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj.set_password(serializer.validated_data['new_password'])
        user_obj.save()
        
        return Response({"success": "Password reset successfully"}, status=status.HTTP_200_OK)
 