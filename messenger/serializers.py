from rest_framework import serializers ,exceptions 
from .models import Conversation , ConversationMessage
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from sport.models import Course
from account.api.v1.serializers import UserAPIViewSerializer

class CreateConversationSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True,max_length=1000)
    class Meta:
        model = Conversation
        fields = ("sender","receiver","title","message")

    def validate(self,attrs):
        sender = attrs.get('sender')
        receiver = attrs.get('receiver')

        if not (Course.objects.filter(teacher__id__in=[sender.id,receiver.id] , student__id__in=[sender.id,receiver.id])):
            raise serializers.ValidationError({'detail':'sender and receiver must have a mutual course'})

        return attrs