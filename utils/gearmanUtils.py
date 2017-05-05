#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gearman import GearmanClient
from commenUtils import client_worker
from functools import wraps

class GearmanClientWrapper:
    def __init__(self, worker_name):
        self.gearman_call_times = 0
        self.worker_name = worker_name 
        self.client = GearmanClient(
                gm_conf_dict[self.worker_name]['host'])

    def refresh_client(self):
        self.gearman_call_times+=1
        if self.gearman_call_times == 50:
            self.gearman_call_times=0
            self.client.shutdown()
            self.client = GearmanClient(gm_conf_dict[self.worker_name]['host'])

def GearmanClientWrapper(func):
    call_times=0
    @wraps(func)
    def wrapper(*args, **kw):
        client = GearmanClient(client_worker)
        pass
    return wrapper

@GearmanClientWrapper
def hf_html_parse_api(filetext, siteId):
    worker_name = "grab_basic"
    packType = "msgpack"
    return aaa


def packRequest(req):
    pass

def unpackResponse(res):
    pass













