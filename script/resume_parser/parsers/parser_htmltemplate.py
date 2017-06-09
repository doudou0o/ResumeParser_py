#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging

from resume_parser.utils.GearmanUtils import hf_html_parse_api as htmltemplate_api
from resume_parser.parsers import parser_five1

logger = logging.getLogger("mylog")

def parse(filename, filetext, fileori):
    logger.debug("html parser run a mission:%s" % filename)
    logger.info("htmltemplate parser return null: it is templary closed")
    return None

    if not filename or not fileori or not filename.endswith("html"):
        logger.info("htmltemplate parser return null: filename is not satisfied or no fileori")
        return None

    sids = taste_site(fileori, filetext)

    if not sids:
        logger.info("htmltemplate parser return null: not any siteid found")
        return None

    for sid in sids:
        result = get_remote_htmltemplate_ret(fileori, sid)
        if result and len(result["work"]) < 1 and len(result["education"]) < 1:
            continue
        if result: break
    else:
        logger.info("htmltemplate parser return null: no result from remote server")
        return None

    return revert_htmlret_to_result(result)

def revert_htmlret_to_result(html_ret):
    # TODO
    html_ret["parser_name"] = "hf_html_parse_api"
    return html_ret


def get_remote_htmltemplate_ret(fileori, sid):
    try:
        gm_response = htmltemplate_api(fileori, sid)
        if gm_response["response"]["err_no"] == 0:
            result = gm_response["response"]["results"]
            if result: return result
    except Exception as e:
        logger.error("remote htmltemplate has raise some exceptions" + e.message)
        return None
    else:
        return None

def taste_site(fileori, filetext):
    sites = []
    if len(re.findall("zhaopin\.(com|cn)", fileori)) > 3:
        sites.append(SiteId.S_ZHAOPIN.value)
    elif parser_five1.match(filetext):
        sites.append(SiteId.S_ZHAOPIN.value)

    if len(re.findall("51job\.com", fileori)) > 5 or\
            len(re.findall("cid:", fileori)) > 8 or len(re.findall("51jobcdn", fileori)) > 5:
        sites.append(SiteId.S_FIVE1.value)

    if len(re.findall("dajieimg\.com", fileori)) > 5:
        sites.append(SiteId.S_DAJIE.value)

    if len(re.findall("chinahr", fileori)) > 4:
        sites.append(SiteId.S_ZHONGHUA.value)

    if len(re.findall("58\.com", fileori)) > 5:
        sites.append(SiteId.S_58TONGC.value)

    if len(re.findall("lietou-edm", fileori)) > 5:
        sites.append(SiteId.S_LIEPIN.value)

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

