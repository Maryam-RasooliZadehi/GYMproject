from django.urls import path , include
from . import views
app_name="sport-api-v1"

urlpatterns = [
    path('course/',views.CourseAPIView.as_view(),name='courses'),
    path('action/',views.ActionListAPIView.as_view(),name='actions'),
    path('diet/',views.DietAPIView.as_view(),name='diets'),
    path('diet/<int:id>/',views.UpdateDietAPIView.as_view(),name='update-diets'),
    path('plan/',views.PlanAPIView.as_view(),name='plans'),
    path('plan/<int:id>/',views.UpdatePlanAPIView.as_view(),name='update-plans'),
    ]