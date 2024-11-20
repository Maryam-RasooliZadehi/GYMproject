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

class DietSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["created_date", "updated_date"]
    #cheecks to see if the user who requests to make a diet is the teacher of the course or not.
    def validate(self, attrs):
        course = attrs.get('course')
        if course.teacher != self.context['request'].user:
            raise serializers.ValidationError({"detail":"you are noit the teacher of this course."})
        return super().validate(attrs)