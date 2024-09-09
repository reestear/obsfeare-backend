from bson import ObjectId
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


# Custom JSON encoder to handle ObjectId
class MongoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


# Custom JsonResponse class
class DecoratedResponse(JsonResponse):
    def __init__(self, data, status_code=200, safe=True, **kwargs):

        super().__init__(
            data,
            encoder=MongoEncoder,
            safe=safe,
            status=status_code,
        )
