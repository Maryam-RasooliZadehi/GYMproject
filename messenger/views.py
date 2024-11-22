# Create your views here.
from rest_framework.response import Response
from .models import Conversation
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

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