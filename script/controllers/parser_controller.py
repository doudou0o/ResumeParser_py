#!/usr/bin/env python
# -*- coding: utf-8 -*-

from convert import getConvertFunc
from script.parsers import get_parser
from script.parsers import parsernames

def run(self, req):
    filename = req["filename"]
    filetext = req["filetext"]
    fileori  = req["fileori"]

    # temporary module of convert file
    if not filetext:
        convert = getConvertFunc(filename.split(".")[-1])
        filetext = convert(fileori)
    
    parsers = (get_parser(t) for t in parsernames)

    results = (parser(filetext, filename) for parser in parsers)

    final_result = merge_results(results)

    return final_result


def merge_results(results):
    """
    itype: results: list[dict(resume)]
    rtype: dict(resume)
    """
    # TODO
    return results[0]


def getErrmsgByReq(self, req):
    """
    :itype req: dict{}
    :rtype  : unicode (if req is valid return "")
    """
    if "filename" not in req:
        return "no filename item in req"
    if "filetext" not in req or not req["filetext"]:
        return "no filetext item in req"
    if "fileori" not in req:
        return "no fileori item in req"

    return ""

def checkRequest(self, req):
    """
    :itype req: dict{}
    :rtype boolean
    """
    return self.getErrmsgByReq(req) == ""



