# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    """
    A serializer for registering a new user.
    Handles all validation, including password confirmation and uniqueness checks.
    """
    # We add two extra fields for password confirmation that are not in the User model.
    # They are write_only so they are used for validation but never shown in an API response.
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        # List the fields the client should send.
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """
        This method is called to perform cross-field validation.
        Here, we check if the two password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs

    def create(self, validated_data):
        """
        This method is called when .save() is called on the serializer.
        It defines how to create the User object from the validated data.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Use set_password() to ensure the password is properly hashed.
        user.set_password(validated_data['password'])
        user.save()

        return user