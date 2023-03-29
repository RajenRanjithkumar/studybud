from django.urls import path
from . import views  

#connect this url file to the root url file(under studybud) 

urlpatterns = [

    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>', views.getRoom),

]