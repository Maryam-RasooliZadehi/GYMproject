from django.urls import path
from . import views 

app_name = "support"

urlpatterns = [
    path('conversations/', views.ConversationAPIView.as_view(),name='conversations'),
    path('conversations/<int:id>/', views.ConversationDetailAPIView.as_view(),name='conversation-details'),
]