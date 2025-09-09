from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _


class JWTFromLocalStorageAuthentication(BaseAuthentication):
    """
    Authentication class that reads JWT token from localStorage via JavaScript
    """
    
    def authenticate(self, request):
        # Check if there's a JWT token in the request headers
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Use JWT authentication to validate the token
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                return (user, validated_token)
            except (InvalidToken, TokenError):
                return None
        
        return None


class SessionOrJWTAuthentication(BaseAuthentication):
    """
    Authentication class that supports both Session and JWT authentication
    """
    
    def authenticate(self, request):
        # First try JWT authentication
        jwt_auth = JWTFromLocalStorageAuthentication()
        jwt_result = jwt_auth.authenticate(request)
        if jwt_result:
            return jwt_result
        
        # Then try session authentication
        if hasattr(request, 'user') and request.user.is_authenticated:
            return (request.user, None)
        
        return None


