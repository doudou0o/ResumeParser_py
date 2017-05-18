#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging

logger = logging.getLogger("mylog")

from resume_parser.utils.GearmanUtils import hf_html_parse_api as htmltemplate_api

def parse(filename, filetext, fileori):
    print "html parser"

    if not filename or not fileori or not filename.endswith("html"):
        logger.debug("htmltemplate parser return null: filename is not satisfied")
        return None

    sids = taste_site(fileori)

    if not sids:
        logger.debug("htmltemplate parser return null: not any siteid found")
        return None

    for sid in sids:
        result = get_remote_htmltemplate_ret(fileori, sid)
        if len(result["work"]) < 1 and len(result["education"]) < 1:
            continue
        if result: break
    else:
        return None

    return revert_htmlret_to_result(result)

def revert_htmlret_to_result(html_ret):
    # TODO
    return html_ret


def get_remote_htmltemplate_ret(fileori, sid):
    gm_response = htmltemplate_api(fileori, sid)
    try:
        if gm_response["response"]["err_no"] == 0:
            result = gm_response["response"]["results"]
            if result: return result
    except:
        pass
    else:
        return None

def taste_site(fileori):
    sites = []
    if len(re.findall("zhaopin\.(com|cn)", fileori)) > 3:
        sites.append(SiteId.S_ZHAOPIN.value)

    if len(re.findall("51job\.com", fileori)) > 5 or len(re.findall("cid:", fileori)) > 8:
        sites.append(SiteId.S_FIVE1.value)

    if len(re.findall("dajieimg\.com", fileori)) > 5:
        sites.append(SiteId.S_DAJIE.value)

    if len(re.findall("chinahr", fileori)) > 4:
        sites.append(SiteId.S_ZHONGHUA.value)

    if len(re.findall("58\.com", fileori)) > 5:
        sites.append(SiteId.S_58TONGC.value)

    return sites



from enum import Enum
class SiteId(Enum):
    S_ZHAOPIN   = 1
    S_FIVE1     = 2
    S_LIEPIN    = 3
    S_DAJIE     = 4
    S_ZHONGHUA  = 9
    S_LAGOU     =11
    S_58TONGC   =12
    S_GANJI     =13
    S_LINGYING  =20

