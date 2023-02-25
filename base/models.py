from django.db import models
from django.contrib.auth.models import User
# Create your models here.



# Data class

class Topic(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
 

# this creates a table with specified attributes
class Room(models.Model):

    host = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True) #SET_NULL will set the contents to null if a room is deleted
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants = 
    updated = models.DateTimeField(auto_now = True) 
    created = models.DateTimeField(auto_now_add = True) # this will just save the time when it was created


    # to put the recently created room at the top
    class Meta:
        ordering = ["-updated", "-created"]

    def __str__ (self):
        return self.name

class Message(models.Model):

    #user 
    # CREATE a relationship with the room class
    # When a room is deleted, all the messages gets deleted

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE) 
    
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True) 
    created = models.DateTimeField(auto_now_add = True) # this will just save the time when it was created

    def __str__ (self):
        return self.body[0:50] # return first 50 character for the preview