#coding: utf-8
from flask import request,jsonify
from common.config import Config
import functools,hmac,base64
from hashlib import sha1
"""
@file: check_data.py
@time: 2017/5/17 
@author: chenfan
"""

conf = Config()

def check():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sha_val = request.headers.get('X-Hub-Signature')
            body = request.get_data()
            #print body
            key = conf.hash_key
            r = hmac.new(key, body, sha1).digest()
            local_sha_val = 'sha1=' + (base64.b16encode(r)).lower()
            print local_sha_val
            if sha_val == local_sha_val:
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'authentication failed'}),400
        return wrapper
    return decorator


