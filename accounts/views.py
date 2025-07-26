from django.shortcuts import render

# Create your views here.
# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

# Use a Class-Based View for concise, standard-compliant code.
# generics.CreateAPIView is specifically designed for "create-only" endpoints.
class RegisterView(generics.CreateAPIView):
    """
    An API endpoint for creating a new user.
    """
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,) # Anyone should be able to register.

    # We can override the default post method to return a custom success message.
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # The serializer's is_valid() method now runs all our checks!
        # - Password confirmation
        # - Username uniqueness (built into ModelSerializer)
        # - Email uniqueness (built into ModelSerializer)
        if serializer.is_valid():
            user = serializer.save() # .save() calls our .create() method.
            return Response(
                {"message": f"User '{user.username}' created successfully. Please log in."},
                status=status.HTTP_201_CREATED
            )
        
        # If not valid, it automatically returns a detailed JSON error response.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)