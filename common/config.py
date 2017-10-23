#coding: utf-8

"""
@file: config.py
@time: 2017/5/17 
@author: chenfan
"""

class Config():
    #zbx server
    zbx_online_server = 'http://172.26.4.36'
    zbx_perf_server = 'http://172.26.4.36'
    zbx_offline_server = 'http://172.26.4.36'
    zbx_user = 'chenfan'
    zbx_pwd = '****'

    #group
    bjzw_g = 'prod'
    bjyz_g = 'stage'
    tjhy_g = 'pref'
    cq_g = 'test'
    defaule_g = 'Discovered hosts'

    #temple
    bjzw_t = 'prod'
    bjyz_t = 'stage'
    tjhy_t = 'pref'
    cq_t = 'test'
    defaule_t = 'linux7 system base template'

    #hash
    hash_key = '*****'

