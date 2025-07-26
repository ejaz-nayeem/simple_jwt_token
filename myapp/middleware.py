# your_app/middleware.py
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import AccessTokenBlacklist
from django.http import JsonResponse

class TokenBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # We only care about requests that have an Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                # Use DRF's JWTAuthentication to validate and decode the token
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(auth_header.split(' ')[1])
                
                # Get the JTI from the validated token
                jti = validated_token.get('jti')
                
                # Check if this JTI is in our blacklist
                if jti and AccessTokenBlacklist.objects.filter(jti=jti).exists():
                    # If it is, reject the request
                    return JsonResponse(
                        {"detail": "Token is blacklisted and invalid."}, 
                        status=401
                    )
            
            except (InvalidToken, TokenError):
                # If the token is invalid for any other reason, let DRF handle it
                pass
        
        # If no token or not blacklisted, continue processing the request
        return None