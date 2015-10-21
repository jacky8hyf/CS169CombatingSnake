from django.http import JsonResponse
from django.core.exceptions import *

def e(err, msg, status_code = 400):
	js = JsonResponse();
	js.status_code = status_code;
	return js

class Error(BaseException, JsonResponse):
    def __init__(self, err, msg, status_code = 400):
        JsonResponse.__init__(self, {'err':err, 'msg':msg})
        BaseException.__init__(self, '{}: {}'.format(err, msg))
        self.status_code = status_code

class Errors:
    NOT_IMPLEMENTED =       Error(-500, 'Not implemented',          500);
    USERNAME_NOT_VALID =    Error(-499, 'Username is not valid',    403);
    USERNAME_TAKEN =        Error(-498, 'Username is taken',        400);
    INCORRECT_PASSWORD =    Error(-496, 'Incorrect password',       403);
    UNKNOWN_USER_ERROR =    Error(-490, 'Unknown error',            400);
    NOT_LOGGED_IN =         Error(-489, 'Not logged in',            403);
    PERMISSION_DENIED =     Error(-403, 'Permission denied',        403); # generic permission denied
    # FIXME more errors

    @staticmethod
    def MISSING_ARGS(arg):
        return Error(-492, 'missing argument {}'.format(arg), 400);
    @staticmethod
    def WRONG_TYPE(arg):
        return Error(-491, 'argument {} has wrong type'.format(arg), 400);

errors = Errors()

class ErrorMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, Error):
            return exception
        if isinstance(exception, FieldError):
            print exception
            return Errors.UNKNOWN_USER_ERROR
        return None
