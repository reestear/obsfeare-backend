from adrf.decorators import api_view
from obsfeare_server.app.repositories import history_repository
from obsfeare_server.app.utils.auth_utils import IsAuthenticated, JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from ..utils.decorated_response_utils import DecoratedResponse


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
async def index(request):
    print("Retrieving Chat History")
    chat_history = await history_repository.get_histories(
        request.user.id
    )  # Use request.user.id now

    if chat_history is None:
        return DecoratedResponse(
            {"message": "Failed to retrieve chat history"},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return DecoratedResponse(
        {
            "chatHistory": chat_history,
            "message": "Successfully retrieved the chat history",
        },
        safe=False,
    )
