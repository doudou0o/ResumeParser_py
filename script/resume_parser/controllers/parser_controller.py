#!/usr/bin/env python
# -*- coding: utf-8 -*-

from convert import getConvertFunc

from resume_parser.parsers import get_parser
from resume_parser.parsers import parsernames

def run(req):
    filename = req["filename"]
    filetext = req["filetext"]
    fileori  = req["fileori"]

    # temporary module of convert file
    if not filetext:
        convert = getConvertFunc(filename.split(".")[-1])
        filetext = convert(fileori)
        if len(filetext) < 20:
            raise Exception("file text is too short!!")

    filetext = clean_filetext(filetext) 

    parsers = (get_parser(t) for t in parsernames)

    results = map(lambda p: p.parse(filename,filetext,fileori), parsers)

    final_result = merge_results(results)

    return final_result


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
    if "filetext" not in req or not req["filetext"]:
        return "no filetext item in req"
    if "fileori" not in req:
        return "no fileori item in req"

    return ""

def checkRequest(req):
    """
    :itype req: dict{}
    :rtype boolean
    """
    return getErrmsgByReq(req) == ""

def clean_filetext(filetext):
    lines = []
    for line in filetext.split("\n"):
        line = line.strip()
        if len(line) < 2:
            continue
        else:
            lines.append(line)
    return "\n".join(lines)


if __name__ == '__main__':
    import sys
    filepath = sys.argv[1]
    req={}
    req["filename"] = filepath.split("/")[-1]
    req["fileori"] = open(filepath).read()
    req["filetext"] = ""
    print run(req)

