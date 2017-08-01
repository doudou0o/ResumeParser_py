#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import quopri
import re
import sys

class MHT2html():
    def __init__(self):
        self.boundary = ""
        self.contents = ""
        self.charset = ""
        self.Transfer_Encoding = ""
        self.html_contents = ""

    def extract(self, content):
        content = re.sub(u"Content-Type: multipart/related;\s*(\r?)\n\s*boundary",
                "Content-Type: multipart/related;boundary",
                content)

        self.contents = content.split("\n")
        self.get_html_content()
        self.transfer_html_content()
        self.decode_html_content()

        self.html_contents = re.sub(">",">\n",self.html_contents)
        return self.html_contents

    def get_html_content(self):
        html_start = False
        header = False
        for line in self.contents:
            ori_line = line
            line = self.remove_blank(line)
            if self.find_boundary(line):
                if html_start:
                    break
                header = True
            if header and self.find_type_html(line):
                html_start = True
            if header and self.find_charset(line):
                print "get charset"
            if header and self.find_transfer_encoding(line):
                print "get Transfer_Encoding"
            if header and line == "":
                header = False
            if not header and html_start:
                self.html_contents += ori_line.strip()


    def transfer_html_content(self):
        if not self.html_contents or not self.Transfer_Encoding:
            return
        if self.Transfer_Encoding == "base64":
            self.html_contents = base64.b64decode(self.html_contents)
        elif self.Transfer_Encoding == "quoted-printable":
            self.html_contents = quopri.decodestring(self.html_contents)
        else:
            print "unknow Transfer_Encoding: %s" % self.Transfer_Encoding


    def decode_html_content(self):
        if not self.html_contents or not self.charset:
            return
        if self.charset == "gb2312":
            self.html_contents = self.html_contents.decode("gbk")
        elif self.charset == "gbk":
            self.html_contents = self.html_contents.decode("gbk")
        elif self.charset == "utf8":
            self.html_contents = self.html_contents.decode("utf8")
        #elif self.charset == "us-ascii":
        #    self.html_contents = self.html_contents.decode("ascii")
        #    self.html_contents = re.sub("&#(?P<num>\d{4,6});", unicode_decode, self.html_contents)
        else:
            print "unknow charset: %s" % self.charset

    def find_boundary(self, line):
        if self.boundary == "":
            m = re.search('Content-Type:multipart/related;boundary="(.+)"', line)
            if m:
                self.boundary = re.sub("-|\s","",m.group(1))
                return False
        else:
            if re.search(self.boundary, line):
                return True
        pass

    def find_type_html(self, line):
        if re.search("Content-Type:text/html", line):
            return True
        else:
            return False

    def find_charset(self, line):
        m = re.search('charset=(.+?)(;|$)', line)
        if m:
            self.charset = re.sub('"', "", m.group(1)).lower()
            return True
        else:
            return False

    def find_transfer_encoding(self, line):
        m = re.search("Content-Transfer-Encoding:(.+)", line)
        if m:
            self.Transfer_Encoding = m.group(1).lower()
            return True
        else:
            return False

    def remove_blank(self, line):
        return re.sub("\s","",line)

    def run(self, content):
        content = re.sub(u"Content-Type: multipart/related;\s*(\r?)\n\s*boundary",
                "Content-Type: multipart/related;boundary",
                content)
        o = MHT2html()
        ret = o.extract(content)
        ret = re.sub(">",">\n",ret)
        return ret

def unicode_decode(matched):
    return unichr(int(matched.group("num")))

if __name__ == '__main__':
    filename = sys.argv[1]
    content = open(filename).read()
    content = re.sub(u"Content-Type: multipart/related;\s*(\r?)\n\s*boundary",
            "Content-Type: multipart/related;boundary",
            content)
    o = MHT2html()
    ret = o.extract(content)
    ret = re.sub(">",">\n",ret)
    print ret



