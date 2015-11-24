# -*- coding: utf-8 -*-
from django.conf import settings
from ws4redis.redis_store import RedisStore, SELF
from ws4redis.subscriber import RedisSubscriber as WS4RedisSubscriber


class RedisSubscriber(WS4RedisSubscriber):
    pass
