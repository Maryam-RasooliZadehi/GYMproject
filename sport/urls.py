from django.urls import path , include

app_name="sport"
urlpatterns = [
    path('api/',include('sport.api.urls'))
    ]