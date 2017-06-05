#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
import logging.config
import gearman
import msgpack
import json

logger = logging.getLogger("mylog")

def unpack_gmrequest(data):
    """
    itype: data: bytes
    rtype: req_dict: dict()
    rtype: packType: str( "magpack" or "json")
    """
    try:
        req_dict = json.loads(data)
        packType = "json"
    except:
        try:
            req_dict = msgpack.unpackb(data)
            packType = "msgpack"
        except:
            req_dict = None
            packType = "json"
    return req_dict, packType

def pack_gmresponse(response, packType):
    if packType == "msgpack":
        return msgpack.packb(response)
    if packType == "json":
        return json.dumps(response)


def check_header(req_dict):
    """
    itype: req_dict: dict()
    rtype: err_msg: unicode (if no err then return "")
    """
    if "header" not in req_dict:
        return "no header in gearman request!!"
    if not req_dict["header"]:
        return "header in gearman request is invalid!!"
    return ""

def getHeaderFromReq(req_dict):
    return req_dict["header"] if "header" in req_dict else None

def getCMPByReq(req_dict):
    """
    itype: req_dict: dict()
    rtype: c,m,p (if no found then return none,none,none)
    """
    c,m,p = None,None,None
    if not "request" in req_dict:
        return c,m,p

    c = req_dict["request"].get("c", None)
    m = req_dict["request"].get("m", None)
    p = req_dict["request"].get("p", None)

    c = c if c else None
    m = m if m else None
    p = p if p else None

    return c,m,p


def assemble_response(header, ERR, err_msg, results):
    err_msg = ERR.value[1]+": "+err_msg
    err_no  = ERR.value[0]

    response = {}
    response["err_no"] = err_no
    response["err_msg"] = err_msg
    response["results"] = results

    ret = {}
    ret["header"] = header
    ret["response"] = response

    logger.info("##### send response: %s" % str(response))
    return ret


def initSourceFile():
    gconf = ConfigParser.ConfigParser()

    # raise Exception
    gconf.read("../conf/source.conf")

    server_conf_file = gconf.get("server", "conf_file")
    logger_conf_file = gconf.get("logger", "conf_file")

    return server_conf_file, logger_conf_file

def initLogger(logger_conf_file):
    # raise Exception
    logging.config.fileConfig(logger_conf_file)
    logger = logging.getLogger("mylog")
    logger.info("logger init sucessful")

def initServerPara(server_conf_file):
    gconf = ConfigParser.ConfigParser()

    # raise Exception
    gconf.read(server_conf_file)

    service_host=gconf.get("gearman", "host")
    service_name=gconf.get("gearman", "name")
    process_num =gconf.get("server", "process_num")

    service_host = service_host.split(",")
    process_num =int(process_num)

    return service_host, service_name, process_num

def init():
    server_conf_file, logger_conf_file = initSourceFile()
    initLogger(logger_conf_file)
    return initServerPara(server_conf_file)

def server_run(server_host, server_name, task_callback):
    gearman_obj = CustomGearmanWorker(server_host)
    gearman_obj.register_task(server_name,task_callback)
    gearman_obj.work()
    pass

class CustomGearmanWorker(gearman.GearmanWorker):
    def on_job_execute(self, current_job):
        return super(CustomGearmanWorker, self).on_job_execute(current_job)
    pass


from enum import Enum
class err_no(Enum):
    ERROR_0 = 0, ""
    ERROR_1 = 1001, "can not unpack gm request"
    ERROR_2 = 1002, "module in request is not exist"
    ERROR_3 = 1003, "no header or header is not valid"
    ERROR_4 = 1004, "request(p) is not valid"
    ERROR_5 = 1005, "request is not satisfied with structure of c,m,p"
    ERROR_6 = 1006, "raise some unknow Exceptions"
    ERROR_7 = 1007, "parse failed"

