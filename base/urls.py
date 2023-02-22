from django.urls import path
from . import views  # import the views from base folder








urlpatterns = [

    path("", views.home, name="home"),
    path("room/<str:pk>", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room")
    
]