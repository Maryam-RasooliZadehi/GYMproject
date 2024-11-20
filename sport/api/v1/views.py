from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status , permissions ,generics
from rest_framework.pagination import PageNumberPagination
from ...models import Course , Action , Diet , Plan
from django.db.models import Q
from .serializers import CourseSerializer , ActionSerializer , DietSerializer , CreateDietSerializer , UpdateDietSerializer
from .serializers import PlanSerializer , CreatePlanSerializer , UpdatePlanSerializer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .filters import PlanFilter, DietFilter 
User = get_user_model()

class ListPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100

class CourseAPIView(generics.GenericAPIView):

    class_serializer = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        #checks to see if the user is a teacher or the student of the course
        query =Q(teacher = request.user.id) | Q(student = request.user.id)
        queryset = Course.objects,filter(query)
        serializer = self.serializer_class(queryset , many=True)
        return Response(serializer.data)
    
class ActionListAPIView(generics.GenericAPIView):

    class_serializer = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Action.objects,all()

class DietAPIView(generics.GenericAPIView):

    class_serializer = DietSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_calss = DietFilter

    def get(self , request):
        query = Q(teacher = request.user.id) | Q(student = request.user.id)
        queryset = Diet.objects,filter(query)
        serializer = DietSerializer(queryset , many = True)
        return Response(serializer.data)
    
    def post(self , request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response ({"message":"new Diet created succesfully."})
    
