#!/usr/bin/env python
# -*- coding: utf-8 -*-


from utils import singleton

"""
DivideModule class
singleton
usage:
1, divide text to content block
2, divide text to exp block
"""
@singleton
class DivideModule():
    def __init__(self):
        pass

    def divideHeadlineBlock(self, headlines=[], isOnly=True):
        """
        :itype: text: unicode
        :itype: headlines: list[unicode]
        :itype: isOnly: boolean
        :rtype: list[[title], unicode]
        """
        pass

    def divideExpBlock(self, timeReg=None ,isOnlt=True):
        """
        :itype: text: unicode
        :itype: timeReg: Pattern
        :itype: isOnly: boolean
        :rtype: list[unicode]
        """
        pass



