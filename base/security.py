#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 7/9/16 11:48 AM

@file:security.py
@author: SPBG Co.,Ltd. ..ing 北京正民惠浩投资管理有限公司 ..ing
"""
import hashlib
import os
import binascii


def get_sha256(msg):
    if isinstance(msg, str):
        bmsg = msg.encode()
        sha = hashlib.sha256(bmsg)
        return sha.hexdigest()
    else:
        raise TypeError('Must be str')


def get_salt(size):
    binsalt = os.urandom(size)
    hexsalt = binascii.hexlify(binsalt)
    return hexsalt.decode()


class Pw(object):
    def __init__(self):
        self.salt = get_salt(32)
        self.password = None

    def encrypt(self, pw, func=lambda pw, salt: pw+salt):
        self.password = pw
        msg = func(self.password, self.salt)
        return get_sha256(msg)
