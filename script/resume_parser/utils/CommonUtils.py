#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import json




"""
单例类装饰器
"""
def singleton(cls, *args, **kw):
    instances = {}
    @wraps(cls)
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


"""
超时方法装饰器
"""
import multiprocessing.pool
def timeout(seconds=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(func, args, kw)
            return async_result.get(seconds)
        return wrapper
    return decorator

"""
worker的IP获取
"""
def client_worker(worker, env=""):
    conf_worker = []
    if env == 'testing':
        conf = open('/opt/wwwroot/conf/gm.conf','r')
    else:
        conf = open('/opt/wwwroot/conf/gm.conf','r')

    conf_dict = json.loads(conf.read())

    if worker in conf_dict:
        if "host" in conf_dict[worker] and type(conf_dict[worker]["host"])==list:
            hosts = conf_dict[worker]["host"]
            for host in hosts:
                conf_worker.append(host)

    return conf_worker

"""
当前环境
"""
def get_env():
    import os
    ipCommen = '''ifconfig|grep 'inet addr:'|awk '{print $2}'|awk -F':' '{print $2}'|grep -v "127.0.0.1"'''
    try:
        LOCALIPs = os.popen(ipCommen).read().strip().split("\n")
    except:
        LOCALIPs = ["127.0.0.1"]

    for ip in LOCALIPs:
        if ip.startswith("192.168.8."):
            return "product"
    for ip in LOCALIPs:
        if ip.startswith("10.9.10."):
            return "testing"
    for ip in LOCALIPs:
        if ip.startswith("192.168.1."):
            return "develop"
    return "unknow"


"""
格式化输出json
"""
def printJson(obj):
    """
    itype: obj : dict
    """
    return json.dump(obj, ensure_ascii=False, sort_keys=True,
            indent=4, separators=(',', ': '))
