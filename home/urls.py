from django.urls import path
from home.views import home, apiResponse

urlpatterns = [
    path('', home, name="home"),
    path('api/', apiResponse, name="API Response")
]
