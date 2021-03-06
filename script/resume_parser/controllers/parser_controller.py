#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from convert import getConvertFunc
from k18 import get_filetext_from_k18
from resume_parser.parsers import get_parser
from resume_parser.parsers import parsernames
from resume_parser import resume_struct

logger = logging.getLogger("mylog")

def run(req):
    filename = req["filename"]
    filetext = req["filetext"]
    fileori  = req["fileori"]

    # temporary module of convert file
    if not filetext:
        start = time.time()
        convert = getConvertFunc(filename.split(".")[-1])
        filetext = convert(fileori)
        logger.info("file text convert finished, using time:%f" % (time.time()-start))
        if filetext is None or len(filetext) < 20:
            logger.warning("file text cannot got, get from k18 next");start = time.time()
            filetext = get_filetext_from_k18(fileori, filename.split(".")[-1])
            logger.warning("file text cannot got, get from k18 finished,using time:%f" % (time.time()-start))
        if filetext is None or len(filetext) < 20:
            raise Exception("file text is too short!!")

    filetext = clean_filetext(filetext)

    parsers = (get_parser(t) for t in parsernames)

    results = map(lambda p: p.parse(filename,filetext,fileori), parsers)
    logger.info("all parser is finished len(results):%d" % len(filter(lambda x:x is not None,results)))

    final_result = merge_results(results)

    if "options" in req and "ret_type" in req["options"] and req["options"]["ret_type"] == "all":
        return final_result

    return resume_struct.clean_result(final_result)


def merge_results(results):
    """
    itype: results: list[dict(resume)]
    rtype: dict(resume)
    """
    # TODO
    for ret in results:
        if ret:
            return ret


def getErrmsgByReq(req):
    """
    :itype req: dict{}
    :rtype  : unicode (if req is valid return "")
    """
    if "filename" not in req:
        return "no filename item in req"
    #if "filetext" not in req or not req["filetext"]:
    #    return "no filetext item in req"
    if "fileori" not in req:
        return "no fileori item in req"

    return ""

def checkRequest(req):
    """
    :itype req: dict{}
    :rtype boolean
    """
    return getErrmsgByReq(req) == ""

from resume_parser.utils import StringUtils
def clean_filetext(filetext):
    lines = []
    for line in filetext.split("\n"):
        line = line.strip()
        line = StringUtils.removeShapesSymbols(line)
        line = StringUtils.removeGeneralPunctuation(line)
        if len(line) < 2:
            continue
        else:
            lines.append(line)
    return "\n".join(lines)


