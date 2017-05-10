#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

class Time_Pair():
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.conj_bt = ""
        self.len_line = 0
        self.oriline = ""

    def GetTimePair(self, time1, time2, line):
        tPair = Time_Pair(time1, time2)
        tPair.serline(line)
        if tPair.islegal():
            return tPair
        else:
            return None

    def setline(self, line):
        self.len_line = len(line)
        self.oriline = line
        self.conj_bt = line[self.time1.pos_e+1: self.time2.pos_s]

    def islegal(self):
        if self.time1.__class__.__name__ != self.time2.__class__.__name__:
            if not self.time2.isSofar():
                return False
        if not self.pos_filter():
            return False
        if not self.conj_filter():
            return False
        if not self.sequence_filter():
            return False
        pass
        return True

    def conj_filter(self):
        """ conj filter
        each conj in times should be same
        the conj between(conj_bt) times should be different from times
        the conj_bt shoud not be number
        """
        if self.conj_bt.isdigit():#TODO 年月 [\.\-~至到~\u2010-\u2015]
            return False
        if self.time2.isSofar():
            return True
        if self.time1.conj != self.time2.conj:
            return False
        if self.conj_bt == self.time1.conj:
            return False
        pass
        return True

    def pos_filter(self):
        """ position filter
        times should not be overlapping
        times should be separated by one or two char

        time_pair should not be in the middle of sentence:
                time_pair pos is in 3 dis from begin or end of line
        """
        Dpos = self.time2.pos_s - self.time1.pos_e -1
        if Dpos < 0: return False;
        if Dpos > 3:
            if len(re.sub(u"[月年]",u"",self.conj_bt)) > 3: # 1991年02月--2010年06月
                return False

        if self.time1.pos_s > 3 and self.len_line - self.time2.pos_e > 3:
            return False
        if re.search(u"[\u4e00-\u9fa5]{2,}",self.oriline[:self.time1.pos_s]):
            return False
        pass
        return True

    def sequence_filter(self):
        """ sequence filter
        time1 should be earlier than time2
        """
        if self.time2.isSofar():
            return True
        try:
            y1,m1 = int(self.time1.year),int(self.time1.month)
            y2,m2 = int(self.time2.year),int(self.time2.month)
        except:
            #logging.error("in sequence_filter, year or month cant change into INT:y1:%s,m1:%s,y2:%s,m2:%s"
            #        % (self.time1.year,self.time1.month,self.time2.year,self.time2.month))
            return False
        if y2 < y1: return False
        if y2 == y1:
            if m2 < m1:
                return False
        pass
        return True

    def toString(self):
        return self.time1.toString()+'-'+self.time2.toString()
