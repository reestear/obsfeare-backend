from obsfeare_server.app.repositories import history_repository
from obsfeare_server.app.utils.auth import IsAuthenticated, JWTAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from ..utils.decorated_response import DecoratedResponse


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    chat_history = history_repository.get_histories(
        request.user.id
    )  # Use request.user.id now

    return DecoratedResponse(chat_history, safe=False)
