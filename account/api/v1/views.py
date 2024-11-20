from rest_framework.response import Response
from copy import copy
from rest_framework import status, permissions, generics
from .serializers import RegistrationSerializer, UserAPIViewSerializer, UpdateUserAPIViewSerializer
from ...models import User


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = copy(serializer.data)
        data.pop("password", None)
        return Response(data, status= status.HTTP_201_CREATED)
    

class UserAPIView(generics.GenericAPIView):
    serializer_class = UpdateUserAPIViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user = request.user
        serializer = UserAPIViewSerializer(user)
        serializer.data['error'] = False
        return Response(serializer.data)
    
    def put(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        User.objects.filter(id = request.user.id).update(**serializer.validated_data)
        return Response({"error":False , "detail":"user updated successfully!"})