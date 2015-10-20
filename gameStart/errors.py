from django.http import JsonResponse

def e(err, msg, status_code = 400):
	js = JsonResponse({'err':err, 'msg':msg});
	js.status_code = status_code;
	return js

class Errors:
    NOT_IMPLEMENTED =       e(-500, 'Not implemented',          500);
    USERNAME_NOT_VALID =    e(-499, 'Username is not valid',    403);
    USERNAME_TAKEN =        e(-498, 'Username is taken',        400);
    # FIXME more errors

errors = Errors()
