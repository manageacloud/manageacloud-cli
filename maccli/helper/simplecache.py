# Simple cache module. Just a dictionary to save key values for this session

import maccli
import hashlib

cache = {}  # Cache dictionary


def get(key):

    if key in cache:
        value = cache[key]
        maccli.logger.debug("Getting %s from cache success: %s" % (key, value))
        return value
    else:
        maccli.logger.debug("Getting %s from cache failed" % key)
        return None


def set_value(key, value):
    maccli.logger.debug("Setting key '%s' with value %s" % (key, value))
    cache[key] = value


def hash_value(value):
    md5 = hashlib.md5(value)
    return md5.hexdigest()