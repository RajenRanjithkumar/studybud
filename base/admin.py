from django.contrib import admin

# Register your models here.


from .models import Room


#add the Room db access to the 
admin.site.register(Room)