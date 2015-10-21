import json
from errors import errors
def parse_json(body):
    try:
        return json.loads(body)
    except ValueError:
        raise errors.MALFORMED_JSON(body)

def assert_type(value, theType):
    if type(value) == theType or isinstance(value, theType): return True
    try:
        theType(value)
        return True
    except ValueError:
        return False

def sanitize_dict(obj, required = dict(), optional = dict()):
    '''
    Requires obj to have certain keys and assert value types. If
    no then throw MISSING_ARGS
    '''
    d = dict()
    for fieldName in required:
        if fieldName not in obj: raise errors.MISSING_ARGS(fieldName)
        if not assert_type(obj[fieldName], required[fieldName]):
            raise errors.WRONG_TYPE(fieldName)
        d[fieldName] = obj[fieldName]
    for fieldName in optional:
        if fieldName not in obj: continue
        if not assert_type(obj[fieldName], optional[fieldName]):
            raise errors.WRONG_TYPE(fieldName)
        d[fieldName] = obj[fieldName]
    return d

