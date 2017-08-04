#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
from suds.client import Client as SoapClient

k18_url="http://cvparse.ifchange.com/ResumeService.asmx?wsdl"
k18_username="u1xxxx"
k18_password="xxxxxx"

def get_filetext_from_k18(fileori, ext):
    """
    return filetext(unicode) from k18 ans
    """
    file_ori_b64 = base64.b64encode(fileori)
    k18_ret = get_k18_result_b64(file_ori_b64, ext)
    if k18_ret is not None and "Original" in k18_ret:
        return k18_ret["Original"]
    else:
        return ""


def get_k18_result_b64(file_ori_b64, ext):
    try:
        ret = SoapClient(k18_url).service.TransResumeByJsonStringForFileBase64(
                username=k18_username,
                pwd=k18_password,
                content=file_ori_b64, ext="."+ext
                )
        ret = json.loads(ret)
    except: ret = None
    return ret


