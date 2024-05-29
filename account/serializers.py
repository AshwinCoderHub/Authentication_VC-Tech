from rest_framework import serializers
from account.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError

from account.utlis import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this because we need to confirm the password field in our Registration Request.
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # Validating Password & Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
    
    class Meta:
        fields = ['password', 'password2'] 
        
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        user.set_password(password)
        user.save()
        return attrs    
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']
     
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'https://localhost:3000/api/user/reset/'+ uid + '/' + token
            print('Password Reset Link', link)
            #Send Email
            body ='Click Following Link to Reset Password'+link
            data = {
                'subject': 'Reset Your Password',
                'body':body,
                'to_email':user.email
                
            }
            Util.send_email(data)
            return attrs  # Return the validated data
        else:
            raise ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
    
    class Meta:
        fields = ['password', 'password2'] 
        
        
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        uid = self.context.get('uid')
        token = self.context.get('token')
        
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        user.set_password(password)
        user.save()
        return attrs    
 
 
        

