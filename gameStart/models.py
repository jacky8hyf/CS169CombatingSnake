from django.db import models
from utils import *
from hashing_passwords import *
from uuid import uuid4

# Create your models here.

class BaseModel(models.Model):
    def save(self):
        '''
        Save this object to database. Return self for chaining.
        '''
        models.Model.save(self)
        return self

    class Meta:
        abstract = True

    @property
    def primary_key(self):
        raise NotImplementedError()

    @property
    def strId(self):
        return (hex(self.primary_key)[2:]) if self.primary_key is not None else None

    @classmethod
    def find_by_id(cls, id):
        if isinstance(id, basestring):
            id = int(id, 16)
        return cls.objects.get(pk = id)

class User(BaseModel):
    # In views.py, use strId instead.
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 64, unique = True)
    pwhash = models.CharField(max_length = 69)
    nickname = models.CharField(max_length = 64)
    inroom = models.ForeignKey('Room', default = None, null = True)
    session_id = models.CharField(max_length = 32, default = None, null = True)

    @property
    def password(self):
        return None # cannot get the password from the object
    @password.setter
    def password(self, value):
        self.pwhash = make_hash(value)

    @property
    def primary_key(self):
        return self.userId

    @classmethod
    def from_dict(cls, d):
        '''
        Create a User from a dictionary. Only username, password and nickname
        is allowed to be set.
        '''
        d = sanitize_dict(d, required = {
            'username': basestring,
            'password': basestring
        }, optional = {
            'nickname': basestring
        });
        obj = cls();
        for key in d:
            setattr(obj, key, d[key])
        return obj

    @classmethod
    def find_by_username(cls, username):
        return cls.objects.get(username = username)

    @classmethod
    def find_by_session_id(cls, session_id):
        return cls.objects.get(session_id = session_id)

    @classmethod
    def find_by_inroom(cls, room):
        return cls.objects.filter(inroom = room)

    def check_password(self, attemptPassword):
        return check_hash(attemptPassword, self.pwhash)

    def update_profile(self, d):
        '''
        Update the current object from a dictionary. Only password and nickname
        is allowed to be updated. Return self to allow chaining.
        '''
        d = sanitize_dict(d, optional = {
            'password': basestring,
            'nickname': basestring
        });
        for key in d:
            setattr(self, key, d[key])
        return self

    def login(self):
        '''
        Generate and set session_id. Return self to allow chaining.
        '''
        self.session_id = uuid4()
        return self

    def logout(self):
        '''
        Unset session_id. Return self to allow chaining.
        '''
        self.session_id = None
        return self

    def enter_room(self, room):
        '''
        inroom setter. Return self to allow chaining.
        '''
        self.inroom = room
        # FIXME check if room is full by F expressions
        return self

    def exit_room(self, room):
        '''
        inroom setter. Return self to allow chaining.
        Exit the specified room if the user is in that room, otherwise no-op.
        '''
        if self.inroom == room:
            self.inroom = None
        # FIXME consider deleting room here??? it should be done after self.save
        return self

    def to_dict(self, includeProfile = False):
        d = {'userId': self.strId}
        if includeProfile:
            d.update({'nickname': self.nickname})
        return d

class Room(BaseModel):
    # In views.py, use strId instead.
    roomId = models.AutoField(primary_key=True)
    capacity = models.IntegerField(default = 8)
    # 0: waiting; 1: playing. More enum values may be added.
    status = models.SmallIntegerField(default = 0)
    creator = models.ForeignKey(User)
    @property
    def primary_key(self):
        return self.roomId
    @classmethod
    def create_by(cls, creator):
        '''Return a room created by creator'''
        obj = cls()
        obj.creator = creator
        return obj

    def to_dict(self, includeCreatorProfile = False, includeMembers = False, includeMemberProfile = False, membersOnly = False):
        d = dict() if membersOnly else \
            {'roomId': self.strId,
            'capacity': self.capacity,
            'status':self.status,
            'creator':self.creator.to_dict(includeProfile = includeCreatorProfile)}
        if includeMembers or membersOnly:
            d.update({'members': [m.to_dict(includeProfile = includeMemberProfile) for m in self.all_members]})
        return d

    @property
    def all_members(self):
        return User.find_by_inroom(self)

    @classmethod
    def all_rooms(cls):
        return cls.objects.all()






