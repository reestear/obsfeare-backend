import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated as DRFIsAuthenticated


class JWTAuthentication(BaseAuthentication):

    # can return only tuple of user and auth
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Did not find token")

        token = auth_header.split(" ")[1]  # Extract the token part
        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        # Assuming the token contains the 'user_id' to identify the user
        user_id = payload.get("id")

        # Mocking a user object. You should query your database for the real user.
        # For example, if you have a User model, you would do something like:
        # user = User.objects.get(id=user_id)
        # Instead, we'll just return an anonymous user for now.
        user = AnonymousUser()  # Replace with actual user lookup if available
        user.id = user_id  # Attach the user_id to the user object

        return (user, None)  # Return the user if authentication is successful


class IsAuthenticated(DRFIsAuthenticated):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "id", None))
