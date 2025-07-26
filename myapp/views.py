from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import AccessTokenBlacklist


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
class LogoutAndBlacklistAccessTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # The token is available in request.auth because of JWTAuthentication
            token = request.auth
            jti = token.get('jti')

            if jti:
                # Add the JTI to the blacklist
                AccessTokenBlacklist.objects.create(jti=jti)
                return Response({"detail": "Access token successfully blacklisted."}, status=status.HTTP_205_RESET_CONTENT)
            
            return Response({"error": "Token has no JTI."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)