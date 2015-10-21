from django.http import JsonResponse
from django.core.exceptions import *

def e(err, msg, status_code = 400):
	js = JsonResponse();
	js.status_code = status_code;
	return js

class SnakeError(BaseException, JsonResponse):
    def __init__(self, err, msg, status_code = 400):
        JsonResponse.__init__(self, {'err':err, 'msg':msg})
        BaseException.__init__(self, '{}: {}'.format(err, msg))
        self.err = err
        self.status_code = status_code

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.err == other.err

    def __ne__(self, other):
        return not self.__eq__(other)

class SnakeErrors:

    SnakeError = SnakeError

    NOT_IMPLEMENTED =       SnakeError(-500, 'Not implemented',          500);
    USERNAME_NOT_VALID =    SnakeError(-499, 'Username is not valid',    403);
    USERNAME_TAKEN =        SnakeError(-498, 'Username is taken',        400);
    INCORRECT_PASSWORD =    SnakeError(-496, 'Incorrect password',       403);
    UNKNOWN_USER_ERROR =    SnakeError(-490, 'Unknown error',            400);
    NOT_LOGGED_IN =         SnakeError(-489, 'Not logged in',            403);
    PERMISSION_DENIED =     SnakeError(-403, 'Permission denied',        403); # generic permission denied
    # FIXME more errors

    @staticmethod
    def MISSING_ARGS(arg):
        return SnakeError(-492, 'missing argument {}'.format(arg), 400);
    @staticmethod
    def WRONG_TYPE(arg):
        return SnakeError(-491, 'argument {} has wrong type'.format(arg), 400);

    @staticmethod
    def MALFORMED_JSON(arg):
        return SnakeError(-488, 'Malformed JSON {}'.format(arg), 400);

errors = SnakeErrors()

class ErrorMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, SnakeError):
            return exception
        if isinstance(exception, FieldError):
            return Errors.UNKNOWN_USER_ERROR
        print exception
        return None
