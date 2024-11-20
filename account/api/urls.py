from django.urls import path , include

app_name= "account-api"

urlpatterns = [
    path("v1/", include("account.api.v1.urls")),
]