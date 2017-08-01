#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jpype
import os
import re
import zipfile

import html2text as html2text
import mht2html
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

jarPath = os.path.join(os.path.dirname(__file__), "../thirdlibs/convert.jar")

def initJVM():
    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path="+jarPath)
    pdfconvertClass = jpype.JClass("com.echeng.convector.pdfconvector.pdf2text")
    pdfconvertObj   = pdfconvertClass()
    return pdfconvertObj


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
    elif fileext == "docx":
        return convert_docx
    elif fileext == "mht":
        return convert_mht
    else:
        raise Exception("unknown file extention input:%s" % fileext)

def convert_mht(fileori):
    """
    itype: fileori: str
    rtype: unicode
    """
    try:
        html_content = mht2html.MHT2html().extract(fileori)
        return convert_html(html_content.encode("utf8"))
    except:
        text = ""
    return text

def convert_docx(fileori):
    def get_docx_text(path):
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'
        """
        Take the path of a docx file as argument, return the text in unicode.
        """
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = XML(xml_content)

        paragraphs = []
        for paragraph in tree.getiterator(PARA):
            texts = [node.text
                    for node in paragraph.getiterator(TEXT)
                    if node.text]
            if texts: paragraphs.append(''.join(texts))
        return '\n\n'.join(paragraphs)
    pass
    filename = "docxfile.docx"
    filepath = "../tmp/%s_%d.docx" % (filename,os.getpid())
    ''' create docx file '''
    with open(filepath, "w") as fp:
        fp.write(fileori)
        fp.close()

    ''' get docx text '''
    try:
        text = get_docx_text(filepath)
        if text: text = re.sub("[\x00-\x09]", " ", text).strip()
    except:
        text = ""

    ''' remove tmp file '''
    cmd = "rm %s" % filepath
    os.system(cmd)

    return text

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

def convert_pdf(fileori, restart=True):
    """
    itype: fileori: bytes
    rtype: unicode
    """
    try:
        pdfconvertObj = initJVM()
        filetext = pdfconvertObj.convert(fileori)
        return filetext
    except:
        if restart:
            return convert_pdf(fileori, False)
        else:
            raise Exception("pdf convert was break down")


if __name__ == '__main__':
    import sys; filepath = sys.argv[1]
    fileori = open(filepath).read()
    print getConvertFunc(filepath.split(".")[-1])(fileori)
