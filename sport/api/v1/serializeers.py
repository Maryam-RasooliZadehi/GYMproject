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
    #checks to see if the user who requests to make a diet is the teacher of the course or not.
    def validate(self, attrs):
        course = attrs.get('course')
        if course.teacher != self.context['request'].user:
            raise serializers.ValidationError({"detail":"you are noit the teacher of this course."})
        return super().validate(attrs)
    
class UpdateDietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = ["start_date","end_date","description"]

    def validate(self, attrs):
        if self.isinstance.course.teacher != self.context["request"].user:
            raise serializers.ValidationError({"detail":"you are not the teacher of the course to edit this diet."})
        return super().validate(attrs)
