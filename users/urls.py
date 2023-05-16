from django.urls import path, include 
from .views import RegisterAPI

urlpatterns =[
    path('auth/', include('dj_rest_auth.urls')),   # dj-rest-auth bunu kısalttık
    path("register/", RegisterAPI.as_view())
]