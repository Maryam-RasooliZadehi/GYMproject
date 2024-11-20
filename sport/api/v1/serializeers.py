from rest_framework import serializers
from ...models import Course, Action , Diet , Plan 
from account.api.v1.serializers import UserAPIViewSerializer

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserAPIViewSerializer()
    student = UserAPIViewSerializer()

    class Meta:
        model = Course
        fields = "__all__"

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"