######################
# Author: Yifan Hong #
######################

from django.db import models
from utils import *
from hashing_passwords import *
from uuid import uuid4
import re
from errors import errors

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
    userId = models.AutoField(max_length = 255, primary_key=True)
    username = models.TextField(max_length = 255, unique = True)
    pwhash = models.TextField(max_length = 255)
    nickname = models.TextField(max_length = 255)
    session_id = models.TextField(max_length = 255, default = None, null = True, unique = True)
    # username = models.TextField(max_length = 255, unique = True)
    # pwhash = models.TextField(max_length = 255)
    # nickname = models.TextField(max_length = 255)
    # session_id = models.TextField(max_length = 255, default = None, null = True, unique = True)

    inroom = models.ForeignKey('Room', max_length = 255, default = None, null = True, on_delete=models.SET_NULL)


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
    def sanity_check_profile_args(cls, d):
        fieldlenstr = lambda x: str(cls._meta.get_field(x).max_length)
        # Implementation notes: Yes we can use a simple length and content check,
        # but a regex is more general to define
        def check(key, pat, errfunc):
            if key in d and d[key] and not re.compile(pat).match(d[key]):
                raise errfunc(d[key])
        check('username',
            '^\w{4,' + fieldlenstr('username') + '}$',
            lambda x: errors.USERNAME_NOT_VALID('{} must be from 4 to {} alphanumeric characters'
                .format(x, fieldlenstr('username'))))
        check('password',
            '^.{4,}$',
            lambda x: errors.PASSWORD_NOT_VALID('must be more than 4 characters'))
        check('nickname',
            '^.{,' + fieldlenstr('nickname') + '}$',
            lambda x: errors.NICKNAME_NOT_VALID('{} must be less than {} characters'
                .format(x, fieldlenstr('nickname'))))

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
        cls.sanity_check_profile_args(d)
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
        self.sanity_check_profile_args(d)
        for key in d:
            setattr(self, key, d[key])
        return self

    def login(self):
        '''
        Generate and set session_id. Return self to allow chaining.
        '''
        self.session_id = str(uuid4())
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

    STATUS_PLAYING = 1
    STATUS_WAITING = 0

    # In views.py, use strId instead.
    roomId = models.AutoField(primary_key=True)
    capacity = models.IntegerField(default = 8)
    # 0: waiting; 1: playing. More enum values may be added.
    status = models.SmallIntegerField(default = STATUS_WAITING)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def destroy_if_created_by(self, user):
        '''
        Delete myself if created by user. Return None because there is no point
        of chaining.
        '''
        if self.creator != user:
            return
        self.delete() # this will sets all member users' inroom attribute to null

    def reassign_creator_if_created_by(self, user):
        if self.creator != user:
            return
        pass # FIXME need to reassign the creator of the room

    def switch_status(self, newStatus):
        '''
        Switch status to a new status. Return self to allow chaining.
        '''
        self.status = newStatus
        return self

    def raise_if_cannot_join(self, user):
        '''
        Determine if a user can join the room. Raise an appropriate exception
        if the user cannot join the room. Return self to allow chaining.
        '''
        # currently all users can join waiting room with spaces
        if self.status != Room.STATUS_WAITING:
            raise errors.ROOM_PLAYING
        if len(self.all_members) >= self.capacity - 1: # -1 for the creator
            raise errors.ROOM_FULL
        return self


