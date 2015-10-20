from django.db import models
from utils import *
from hashing_passwords import *

# Create your models here.

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 64)
    pwhash = models.CharField(max_length = 69)
    nickname = models.CharField(max_length = 64)
    inroom = models.ForeignKey('Room')
    session_id = models.CharField(max_length = 32, default = None)
    
    @password.setter
    def password(self, value):
        pwhash = make_hash(value)
    
    @classmethod
    def from_dict(cls, d):
        d = sanitize_dict(d, required = {
            'username': str,
            'password': str
        }, optional = {
            'nickname': str
        });
        obj = cls();
        for key in d:
            setattr(obj, key, d[key])
        return obj
    
    def update
    
class Room(models.Model):
    roomId = models.AutoField(primary_key=True)
    capacity = models.IntegerField(default = 8)
    # 0: waiting; 1: playing. More enum values may be added.
    status = models.SmallIntegerField(default = 0)
    creator = models.ForeignKey(User)

    
    