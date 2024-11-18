from rest_framework.response import Response
from copy import copy
from rest_framework import status, permissions, generics
from .serializers import RegistrationSerializer, UserAPIViewSerializer, UpdateUserAPIViewSerializer
from ...models import User


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serlizer = self.serializer_class(data = request.data)
        serlizer.is_valid(raise_exception=True)
        serlizer.save()
        data = copy(serlizer.data)
        data.pop("password", None)
        return Response(data, status= status.HTTP_201_CREATED)