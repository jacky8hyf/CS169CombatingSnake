from django.http import JsonResponse
from django.core.exceptions import *
from django.db import models as django_models

import inspect

import models as snake_models

def e(err, msg, status_code = 400):
	js = JsonResponse();
	js.status_code = status_code;
	return js

class SnakeError(Exception, JsonResponse):
    def __init__(self, err, msg, status_code = 400):
        Exception.__init__(self, '{}: {}'.format(err, msg))
        JsonResponse.__init__(self, {'err':err, 'msg':msg})
        self.err = err
        self.status_code = status_code

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.err == other.err

    def __ne__(self, other):
        return not self.__eq__(other)

class SnakeErrors:

    SnakeError = SnakeError

    NOT_IMPLEMENTED =       SnakeError(-501, 'Not implemented',          500);
    USERNAME_TAKEN =        SnakeError(-498, 'Username is taken',        400);
    INCORRECT_PASSWORD =    SnakeError(-496, 'Incorrect password',       403);
    UNKNOWN_USER_ERROR =    SnakeError(-490, 'Unknown error',            400);
    ROOM_FULL =             SnakeError(-494, 'Room is full',             400);
    ROOM_PLAYING =          SnakeError(-493, 'Game in progress',         400);
    NOT_LOGGED_IN =         SnakeError(-489, 'Not logged in',            403);
    PERMISSION_DENIED =     SnakeError(-403, 'Permission denied',        403); # generic permission denied

    USERNAME_NOT_VALID = lambda self, arg: \
        SnakeError(-499, 'Username is not valid{}'.format(': {}'.format(arg) if arg else ''), 400);

    PASSWORD_NOT_VALID = lambda self, arg: \
        SnakeError(-497, 'Password is not valid{}'.format(': {}'.format(arg) if arg else ''), 400);

    NICKNAME_NOT_VALID = lambda self, arg: \
        SnakeError(-495, 'Nickname is not valid{}'.format(': {}'.format(arg) if arg else ''), 400);

    MISSING_ARGS = lambda self, arg: \
        SnakeError(-492, 'missing argument {}'.format(arg), 400);

    WRONG_TYPE = lambda self, arg: \
        SnakeError(-491, 'argument {} has wrong type'.format(arg), 400);


    @staticmethod
    def MALFORMED_JSON(arg):
        return SnakeError(-488, 'Malformed JSON {}'.format(arg), 400);

    @staticmethod
    def INTERNAL_SERVER_ERROR(arg):
        return SnakeError(-500, 'Internal Server Error {}'.format(arg), 500);

    @staticmethod
    def DOES_NOT_EXIST(arg):
        return SnakeError(-404, 'Not Found {}'.format(arg), 404);

errors = SnakeErrors()
import traceback
class ErrorMiddleware(object):
    # FIXME: this middleware is not catching SnakeError!
    def process_exception(self, request, exception):
        if not exception:
            return None
        for name, t in inspect.getmembers(snake_models,
            lambda c: inspect.isclass(c) and issubclass(c, django_models.Model)):
            if hasattr(t, 'DoesNotExist') and isinstance(exception, t.DoesNotExist):
                return errors.DOES_NOT_EXIST(t.__name__)
        if isinstance(exception, SnakeError):
            return exception
        # if isinstance(exception, FieldError):
        #     return Errors.UNKNOWN_USER_ERROR
        traceback.print_exc();
        return errors.INTERNAL_SERVER_ERROR('{}: {}'.format(str(type(exception)), str(exception)))
