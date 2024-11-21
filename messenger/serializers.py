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
    

class ConversationSerializer(serializers.ModelSerializer):
    sender = UserAPIViewSerializer()
    receiver = UserAPIViewSerializer()
    class Meta: 
        model = Conversation
        fields = '__all__'


class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ConversationMessage
        fields = '__all__'


class ConversationMessagePaginatorSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)


class ConversationDetailSerializer(serializers.ModelSerializer):
    conversation_messages = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Conversation
        fields = '__all__'
    
    def get_conversation_messages(self, obj):
        request = self.context.get('request')
        paginator_serializer = ConversationMessagePaginatorSerializer(data = request.query_params)
        paginator_serializer.is_valid(raise_exception=True)
        page_size = int(request.query_params.get('page_size', 10))  
        page_number = int(request.query_params.get('page', 1))  
        
        messages = obj.conversationmessage_set.all().order_by('-id')
        paginator = Paginator(messages, page_size)
        page = paginator.get_page(page_number)
        serializer = ConversationMessageSerializer(page.object_list, many=True, read_only=True)
        message_ids = [message.id for message in page.object_list]
        obj.conversationmessage_set.filter(id__in=message_ids).exclude(user=request.user).update(viewed=True)
        data = serializer.data
        data.reverse()
        return {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_number,
            'messages': data
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for message in rep['conversation_messages']['messages']:
            if message['user'] == self.context['request'].user.id:
                message['is_you'] = True
            else:
                message['is_you'] = False
        return rep


class AddMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessage
        fields = ("user","conversation","message")

    def validate(self, attrs):
        valid = super().validate(attrs)
        conversation = attrs.get("conversation")

        if attrs.get("user").id not in [conversation.receiver.id,conversation.sender.id]:
            raise exceptions.ValidationError({"detail":"this conversation is not yours"})

        return valid
