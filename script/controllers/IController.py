#!/usr/bin/env python
# -*- coding: utf-8 -*-




class IController():
    def __init__(self):
        pass


    def getErrmsgByReq(self, req):
        """
        :itype req: dict{}
        :rtype  : unicode (if req is valid return "")
        """
        raise Exception("IController method getErrmsgByReq NotImplemented")

    def checkRequest(self, req):
        """
        :itype req: dict{}
        :rtype boolean
        """
        return  self.getErrmsgByReq(req) == ""

    def run(self, req):
        raise Exception("IController method run NotImplemented")

