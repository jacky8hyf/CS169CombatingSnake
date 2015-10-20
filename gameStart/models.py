from django.db import models

# Create your models here.

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 64)
    pwhash = models.CharField(max_length = 69)
    nickname = models.CharField(max_length = 64)
    inroom = models.ForeignKey('Room')

class Room(models.Model):
    roomId = models.AutoField(primary_key=True)
    capacity = models.IntegerField(default = 8)
    # 0: waiting; 1: playing. More enum values may be added.
    status = models.SmallIntegerField(default = 0)
    creator = models.ForeignKey(User)

    
    