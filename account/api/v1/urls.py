from django.urls import path , include
from . import views
from rest_framework_simplejwt.views import (TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

app_name="account-api-v1"

urlpatterns = [
        # registration 
        path("registration/",views.RegistrationApiView.as_view(),name = 'registration'),
        # user update
        path("user_info/",views.UserAPIView.as_view() , name = "user-info"),
        # login jwt
        path("jwt/create/",TokenObtainPairView.as_view() , name = "jwt-create"),
        path("jwt/refresh/",TokenRefreshView.as_view() , name = "jwt-refresh"),
        path("jwt/verify/",TokenVerifyView.as_view() , name = "jwt-verify"),
    ]