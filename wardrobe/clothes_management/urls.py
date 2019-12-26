from django.urls import path
from clothes_management import views

urlpatterns = [
    path('upload_clothes', views.upload_clothes),
    path('get_clothes', views.get_clothes),
]
