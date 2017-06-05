#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from gearman import GearmanClient
import msgpack
import json


#packType="json"
packType="msgpack"

def packRequest(req):
    if packType == "msgpack":
        return msgpack.packb(req)
    else:
        return json.dumps(req)

def unpackResponse(res):
    if packType == "msgpack":
        return msgpack.unpackb(res)
    else:
        return json.loads(res)

def send_request(WORKERNAME, HOST, POST, REQUEST):
    client = GearmanClient([HOST+":"+str(POST)])
    response = client.submit_job(WORKERNAME,packRequest(REQUEST))
    result = unpackResponse(response.result)
    return result


def buildReq():
    req = {}
    req["header"] = {"uid":"111", "user":"myself"}
    req["request"] = {
            "c":"resume_parse_module",
            "m":"resume_parse",
            "p":{}
            }

    req["request"]["p"]["filename"] = sys.argv[1]
    req["request"]["p"]["filetext"] = ""
    req["request"]["p"]["fileori"] = open(sys.argv[1], "r").read().decode("utf8")

    return req

def run():
    WORKERNAME = "resume_parser_module"
    HOST = "192.168.1.111"
    POST = "4730"

    REQUEST = buildReq()

    ret = send_request(WORKERNAME, HOST, POST, REQUEST)

    print json.dumps(ret, ensure_ascii=False)

def usage():
    return "usage:\n\tpython ecv_parser_gm_client.py filepath"

if __name__ == '__main__':
    if len(sys.argv)-1 != 1:
        print usage()
        exit(0)

    run()


