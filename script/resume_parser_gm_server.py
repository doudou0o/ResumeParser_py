#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import logging
import traceback
import sys

import resume_parser_gm_helper as helper
from resume_parser_gm_helper import err_no

import resume_parser.controllers as controllers

sys.path.append("../utils/")

logger = logging.getLogger("mylog")

def task_callback(GearmanWorker, job):
    # unpack data
    req_dict, packType = helper.unpack_gmrequest(job.data)
    if not req_dict:
        return helper.pack_gmresponse(helper.assemble_response(None, err_no.ERROR_1, "", None), packType)

    logger.info("##### received request: %s" % str(req_dict))

    # preprocess request
    head_err_msg =  helper.check_header(req_dict)
    if head_err_msg:
        return helper.pack_gmresponse(helper.assemble_response(None, err_no.ERROR_3, head_err_msg, None), packType)
    header = helper.getHeaderFromReq(req_dict)

    c, m, p = helper.getCMPByReq(req_dict)
    if not m or not p:
        return helper.pack_gmresponse(helper.assemble_response(header, err_no.ERROR_5, "", None), packType)


    # handle request
    controller = controllers.getController(m)
    if controller is None:
        return helper.pack_gmresponse(helper.assemble_response(header, err_no.ERROR_2, m, None), packType)

    if not controller.checkRequest(p):
        errmsg = controller.getErrmsgByReq(p)
        return helper.pack_gmresponse(helper.assemble_response(header, err_no.ERROR_4, errmsg, None), packType)

    try:
        result = controller.run(p)
    except:
        tb = traceback.format_exc()
        logger.error("the req:%s happened exception:\n,%s" % (header, tb))
        return helper.pack_gmresponse(helper.assemble_response(header, err_no.ERROR_6, tb, result), packType)

    if not result:
        return helper.pack_gmresponse(helper.assemble_response(header, err_no.ERROR_7, "", result), packType)

    return helper.pack_gmresponse(helper.assemble_response(header, err_no.ERROR_0, "", result), packType)



if __name__ == '__main__':
    # init
    server_host, server_name, worker_num = helper.init()

    logger.info("********* server init **************")

    process_list=[]
    for i in xrange(worker_num):
        process_obj = multiprocessing.Process(target=helper.server_run, args=(server_host,server_name,task_callback))
        process_list.append(process_obj)

    # start
    for i in xrange(worker_num):
        process_obj = process_list[i]
        process_obj.start()

    logger.info("********* server start **************")

    # join
    for i in xrange(worker_num):
        process_obj = process_list[i]
        process_obj.join()

    logger.info("********* server exit **************")


