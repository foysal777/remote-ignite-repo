from rest_framework import serializers
from .models import User , Profile
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )
 
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
 
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
 
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )
 
        return value
  





class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    purpose = serializers.ChoiceField(choices=['registration', 'password_reset'])


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)




from rest_framework import serializers
from .models import Profile
 
class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
 
    def validate_profile_picture(self, image):
        if image is None:
            return image
 
        max_size = 20 * 1024 * 1024  # 20 MB
        if image.size > max_size:
            raise serializers.ValidationError(
                "Profile picture size must be less than or equal to 20 MB."
            )
        return image
 
    class Meta:
        model = Profile
        fields = [
            'email',
            'first_name', 'last_name', 'gender', 'profession',
            'date_of_birth', 'profile_picture', 'phone', 'location',
            'personal_email', 'about_yourself', 'professional_background',
            'role'
        ]


from rest_framework import serializers
from accounts.models import User

class UserListSerializer(serializers.ModelSerializer):
    register_date = serializers.DateTimeField(source="created_at")

    class Meta:
        model = User
        fields = ["id", "email", "register_date", "role", "plan_type"]





# add + delete ----------------------  user --------------
# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "role",
            "plan_type",
            "is_plan_paid",
            "plan_start_date",
            "plan_end_date",
            "total_time",
            "extra_prompts",
            "is_active",
            "is_staff",
        ]
        extra_kwargs = {
            "is_staff": {"read_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "role",
            "plan_type",
            "is_plan_paid",
            "plan_start_date",
            "plan_end_date",
            "total_time",
            "extra_prompts",
            "is_active",
        ]
        read_only_fields = ["email"]  

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
