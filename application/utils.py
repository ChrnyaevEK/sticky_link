import hashlib
import json


def get_version(instance):
    version_string = ''
    try:
        version_string = instance.last_update.isoformat()
    except AttributeError:
        pass
    return hashlib.md5(json.dumps(version_string).encode('utf-8')).hexdigest()
