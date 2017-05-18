#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gearman import GearmanClient
import msgpack
import json

from CommonUtils import client_worker



def hf_html_parse_api(fileori, siteId):
    workername = "grab_basic"
    packType = "msgpack"

    request = {}
    request["w"] = "grab_basic"
    request["c"] = "apis/logic_parse"
    request["m"] = "parsers_engine"
    request["d"] = "parsers_engine"
    request["p"] = {
            "body" : fileori,
            "site_id" : siteId,
            "type" : "resume",
            }

    req = {}
    req["header"] = getHeader()
    req["request"] = request

    return send_request(workername, client_worker(workername), req, packType)

def getHeader():
    return {"user":"resume_parser"}


def packRequest(req, packType="msgpack"):
    if packType == "msgpack":
        return msgpack.packb(req)
    else:
        return json.dumps(req)


def unpackResponse(res, packType="msgpack"):
    if packType == "msgpack":
        return msgpack.unpackb(res)
    else:
        return json.loads(res)


def send_request(workername, host, request, packType="msgpack"):
    client = GearmanClient(host)
    response = client.submit_job(workername, packRequest(request, packType))
    result =  unpackResponse(response.result)
    client.shutdown()
    return result
    











