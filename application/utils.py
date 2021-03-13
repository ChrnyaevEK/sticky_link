import hashlib
import json


def get_version_hash(validated_data):
    return hashlib.md5(json.dumps(validated_data).encode('utf-8')).hexdigest()
