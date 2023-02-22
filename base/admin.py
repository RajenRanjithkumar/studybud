from django.contrib import admin

# Register your models here.


from .models import Room, Topic, Message


#add the Room db access to the 
admin.site.register(Room)

#user model is registered by default

admin.site.register(Topic)
admin.site.register(Message)