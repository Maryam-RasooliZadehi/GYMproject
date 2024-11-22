# Create your views here.
from rest_framework.response import Response
from .models import Conversation, ConversationMessage
from django.contrib.auth import get_user_model
from rest_framework import generics ,permissions
from rest_framework.pagination import PageNumberPagination
from .serializers import ConversationSerializer, CreateConversationSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.db.models import Exists, OuterRef, Q, Subquery

User = get_user_model()


class ListPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'new_conversations': Conversation.objects.filter(conversationmessage__viewed=False).exclude(conversationmessage__user=self.request.user.id).distinct().count(),
            'results': data,
        })


class ConversationAPIView(generics.ListAPIView):
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = ConversationSerializer
    pagination_class = ListPagination

    def get_queryset(self):
        query = Q(sender= self.request.user.id) | Q(receiver= self.request.user.id)
        queryset = Conversation.objects.filter(query).annotate(
            not_viewed=Exists(ConversationMessage.objects.filter(
                                                                                                conversation=OuterRef('pk'),
                                                                                                viewed=False
                                                                                            ).exclude(user=self.request.user.id)),
                last_message_id=Subquery(ConversationMessage.objects.filter(conversation=OuterRef('pk')).order_by('-id').values('id')[:1])
                                ).order_by('not_viewed','-last_message_id')
        print(ConversationSerializer(instance=queryset,many=True).data)
        return queryset
    
    @extend_schema(
        description="Get list of user's conversations",
    )
    def get(self,*args,**kwargs):
        return super().get(*args,**kwargs)
        
    @extend_schema(
        responses={status.HTTP_201_CREATED: 'conversation created successfully!'},
        description='Create a conversation from a user',
        examples=[
            OpenApiExample(
                name="body example",
                value={
                            "title": "string Maxlength=50 , Minlength=10",
                            "receiver":"id of receiver's id",
                            "message": "Maxlength=1000",
                            },
                request_only=True,
            )
        ]
    )
    def post(self,request):
        request.data["sender"]=request.user.id
        serializer = CreateConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation_message_data = {"message":serializer.validated_data.pop("message"),
                                                                "user":serializer.validated_data["sender"]}
        conversation = serializer.save()
        conversation.conversationmessage_set.create(**conversation_message_data)
        return Response({"detail": "conversation created successfully!"},status=status.HTTP_201_CREATED)

