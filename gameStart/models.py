######################
# Author: Yifan Hong #
######################

from django.db import models
from django.db.models import F
from utils import *
from hashing_passwords import *
from uuid import uuid4
import re
import random
from combatingSnake.settings import *
from errors import errors, RoomEmptyError

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

    @staticmethod
    def intId_from_strId(strId):
        return int(strId, 16)

    @classmethod
    def find_by_id(cls, id):
        if isinstance(id, basestring):
            id = cls.intId_from_strId(id)
        return cls.objects.get(pk = id)

class User(BaseModel):
    # In views.py, use strId instead.
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 64, unique = True)
    pwhash = models.CharField(max_length = 69)
    nickname = models.CharField(max_length = 64)
    session_id = models.CharField(max_length = 36, default = None, null = True, unique = True)
    inroom = models.ForeignKey('Room', default = None, null = True, on_delete=models.SET_NULL)
    numgames = models.PositiveIntegerField(default = 0)
    numwin = models.PositiveIntegerField(default = 0)

    @property
    def password(self):
        return None # cannot get the password from the object
    @password.setter
    def password(self, value):
        self.pwhash = make_hash(value)

    @property
    def primary_key(self):
        return self.userId

    @property
    def nicknameOrUsername(self):
        '''
        Return nickname if it is not empty, otherwise username
        '''
        return self.nickname or self.username

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
            lambda x: errors.PASSWORD_NOT_VALID('must be at least 4 characters'))
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
        '''
        Return everyone in the room, including the creator.
        '''
        return cls.objects.filter(inroom = room)

    @classmethod
    def update_scores(cls, players, winner = None):
        players = set([cls.intId_from_strId(strId) for strId in players])
        if winner:
            winner = cls.intId_from_strId(winner)
            if winner in players:
                players.remove(winner)
        cls.objects.filter(userId__in = players).update(numgames = F('numgames') + 1)
        if winner:
            cls.objects.filter(userId = winner).update(
                numgames = F('numgames') + 1,
                numwin = F('numwin') + 1)

    @classmethod
    def get_leaderboard(cls):
        '''
        Return a QuerySet of Users ordered by the number of winned games.
        '''
        return cls.objects.all().order_by('-numwin')

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
        Mark user as in specified room. Exit previous rooms. Return self to allow chaining.
        '''
        if self.inroom:
            self.exit_room(self.inroom)
        self.inroom = room
        return self

    def exit_room(self, room):
        '''
        Exit the specified room if the user is in that room, otherwise no-op.
        Will delete the room if the room is empty.
        Return self to allow chaining.
        '''
        if self.inroom == room:
            self.inroom = None
            try:
                room.reassign_creator_if_created_by(self).save()
            except RoomEmptyError:
                pass
        return self

    def to_dict(self, includeProfile = False, includeScores = False):
        d = {'userId': self.strId}
        if includeProfile:
            d.update({'nickname': self.nicknameOrUsername})
        if includeScores:
            d.update({'numgames': self.numgames, 'numwin': self.numwin})
        return d

class Room(BaseModel):

    # In views.py, use strId instead.
    roomId = models.AutoField(primary_key=True)
    capacity = models.IntegerField(default = MAX_MEMBERS_IN_ROOM)
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
        '''
        Return all members in the room, excluding the creator.
        '''
        return [u for u in User.find_by_inroom(self) if u != self.creator]

    @classmethod
    def all_rooms(cls):
        return cls.objects.all()

    def reassign_creator_if_created_by(self, user):
        '''
        If the room is created by the specified user, reassign .creator field
        to some other members in the room. If there is no members left, delete
        the room and raise RoomEmptyError.
        '''

        # print "room {} created by {} is reassigining creator if by {}".format(self.strId, self.creator.strId, user.strId)
        if self.creator != user:
            return self
        members = self.all_members
        if members:
            self.creator = random.choice(members)
        else:
            # print 'deleting room {}'.format(self.strId)
            self.delete()
            raise RoomEmptyError()
        return self

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
        if self.creator == user or user in self.all_members:
            return self
        if self.status != STATUS_WAITING:
            raise errors.ROOM_PLAYING
        if len(self.all_members) >= self.capacity - 1: # -1 for the creator
            raise errors.ROOM_FULL
        return self

