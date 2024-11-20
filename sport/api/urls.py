from django.urls import path , include

app_name="sport-api"
urlpatterns = [
    path('v1/',include('sport.api.v1.urls'))
    ]