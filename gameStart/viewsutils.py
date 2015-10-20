import json
def parse_json(body):
    try:
        return json.loads(body)
    except ValueError:
        return None

def assert_type(value, theType):
    if type(value) == theType: return True
    try:
        theType(value)
        return True
    except ValueError:
        return False

def assert_types(obj, required = dict(), optional = dict()):
    '''
    assert_types
    '''
    for fieldName in required:
        if fieldName not in obj: return False
        if not assert_type(obj[fieldName], required[fieldName]):
            return False

    for fieldName in optional:
        if not assert_type(obj[fieldName], optional[fieldName]):
            return False

    return True

