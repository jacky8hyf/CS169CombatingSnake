import json
def parse_json(body):
    try:
        return json.loads(body)
    except ValueError:
        print "Inside value error"
        return None

def assert_type(value, theType):
    if type(value) == theType: return True
    try:
        theType(value)
        return True
    except ValueError:
        return False

def sanitize_dict(obj, required = dict(), optional = dict()):
    d = dict()
    for fieldName in required:
        if fieldName not in obj: return None
        if not assert_type(obj[fieldName], required[fieldName]):
            return None
        d[fieldName] = obj[fieldName]
    for fieldName in optional:
        if not assert_type(obj[fieldName], optional[fieldName]):
            return None
        d[fieldName] = obj[fieldName]
    return d

