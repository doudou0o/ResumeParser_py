#!/usr/bin/env python
# -*- coding: utf-8 -*-

from convert import getConvertFunc
from script.parsers import five1Parsers
from script.parsers import zhilianParsers
from script.parsers import htmlTemplateParser
from script.parsers import generalParser

def run(self, req):
    filename = req["filename"]
    filetext = req["filetext"]
    fileori  = req["fileori"]

    # temporary module of convert file
    if not filetext:
        convert = getConvertFunc(filename.split(".")[-1])
        filetext = convert(fileori)

    # template parsers
    result_51 = five1Parsers.parse(filetext, filename)
    result_zl = zhilianParsers.parse(filetext, filename)

    # html template parsers
    result_ht = htmlTemplateParser.parse(filetext, filename)

    # general parsers
    result_gp = generalParser.parse(filetext, filename)
    
    # merge each results
    finalRet = mergeResults([result_51,result_zl,result_ht,result_gp])

    return finalRet

def mergeResults(results):
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



