#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jpype
import html2text

def getConvertFunc(fileext):
    """
    itype: fileext: unicode
    rtype: convert function
    """
    if fileext == "txt":
        return convert_text
    elif fileext == "pdf":
        return convert_pdf
    elif fileext == "html":
        return convert_html
    else:
        raise Exception("unknown file extention input")

def convert_html(fileori):
    """
    itype: fileori: str
    rtype: unicode
    """
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_links = True
    ori_text = h.handle(convert_text(fileori))
    return ori_text
    


def convert_text(fileori):
    """
    itype: fileori: str
    rtype: unicode
    """
    try:return fileori.decode("utf8")
    except:
        pass
    try:return fileori.decode("gbk")
    except:
        pass
    raise Exception("text convert can not decode file")

def convert_pdf(fileori):
    """
    itype: fileori: bytes
    rtype: unicode
    """
    try:
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=../")
        pdfconvertClass = jpype.JClass("com.")
        pdfconvertObj   = pdfconvertClass()
        return pdfconvertObj.convert(fileori)
        jpype.shutdownJVM()
        pass
    except:
        jpype.shutdownJVM()
        raise Exception("pdf convert was break down")


