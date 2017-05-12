#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import sys
import re
import logging
import os

dirpath  = os.path.dirname(__file__)
timeconf = os.path.join(dirpath, "timeBNF.conf")

"""TimeBuilders is used as Factory to produce TimeBuilder"""
TimeBuilders = {}

def getTB( tName):
    if tName in TimeBuilders:
        return TimeBuilders[tName]
    else:
        TB = TimeBuilder()
        if TB.build_time(tName) and TB.build_reg(tName):
            TimeBuilders[tName] = TB
            return TB
        else:
            return None


class TimeBuilder():
    """ create concrete Time() object

    1' build_time  get TimeClass
    2' build_reg   get regular of Time()
    3' findall     get all concrete Time() object matched by regular
    """
    def __init__(self):
        self.timeClass = None
        self.reg = ""
        self.conf_info = {}
        self.readConf(timeconf)
        pass

    def new(self):
        pass


    def build_time(self, tName):
        try:
            self.timeClass = getattr(sys.modules[__name__], tName)
            return True
        except:
            #logging.error("can not found class name:%s" % tName)
            return False

    def build_reg(self, tName):
        """parse final regular
        if success return True else return False
        """
        oriStr = self.conf_info["time_reg"][tName]
        reg = self._parse_ori_reg(oriStr)
        if reg != None:
            self.reg = "(?=("+reg+"))"
            return True
        else:
            return False

    def findall(self, strline):
        tObj_list = []
        matches = re.finditer(self.reg, strline)
        for m in matches:
            m_dict = m.groupdict()
            year,month,conj = u"",u"",u""
            if "year" in m_dict:
                year = m.group("year")
            if "month" in m_dict:
                month = m.group("month")
            if "conj" in m_dict:
                conj = m.group("conj")
            pos_start = m.start()
            # set y m c conj
            tObj = self.timeClass(year, month, conj)
            # set len
            tObj.setLen(len(m.group(1)))
            # set pos
            tObj.setPos(pos_start)
            # set range
            year_range  = map(lambda x:int(x), self.conf_info["year_range"])
            month_range = map(lambda x:int(x), self.conf_info["month_range"])
            tObj.setRange(year_range, month_range)

            if tObj_list and tObj.equal(tObj_list[-1]):continue;
            tObj_list.append(tObj)
        #logging.debug("tObj_list:"+str(tObj_list))

        tObj_legel_list = []
        for tObj in tObj_list:
            if tObj.islegal():
                tObj_legel_list.append(tObj)
        #logging.debug("tObj_legel_list:"+str(tObj_legel_list))
        return tObj_legel_list

    def readConf(self, conf_file):
        conf = ConfigParser.ConfigParser()
        conf.optionxform = str
        ans = conf.read(conf_file)
        if not ans:
            #logging.error("not found conf_file:%s" % conf_file)
            return
        # time reg conf
        if "time_reg" not in conf.sections():
            #logging.error("not found session time_reg")
            return
        self.conf_info["token"] = {}
        self.conf_info["syntax"] = {}
        self.conf_info["time_reg"] = {}
        for token in conf.options("token"):
            token_info = conf.get("token",token)
            token_info = self._unicode_info(token_info)
            self.conf_info["token"][token] = token_info
        for syntax in conf.options("syntax"):
            syntax_info = conf.get("syntax",syntax)
            syntax_info = self._unicode_info(syntax_info)
            self.conf_info["syntax"][syntax] = syntax_info
        for time in conf.options("time_reg"):
            time_info = conf.get("time_reg",time)
            time_info = self._unicode_info(time_info)
            self.conf_info["time_reg"][time] = time_info
        # time range conf
        if "time_range" not in conf.sections():
            #logging.error("not found session time_range")
            return
        self.conf_info["year_range"] = conf.get("time_range", "year_range").split(",")
        self.conf_info["month_range"] = conf.get("time_range", "month_range").split(",")

    def _unicode_info(self, line):
        line = line.decode("utf8")
        for unicode_str in re.findall("\\\\u\d{4}", line):
            new_unicode = unicode_str.decode("unicode_escape")
            line = line.replace(unicode_str,new_unicode)
            line = re.sub("\s","",line)
        return line

    def _parse_ori_reg(self, oriStr, l=0):
        match_iter = re.finditer("(?<!\?P)<(.+?)>", oriStr)
        final_reg = oriStr
        for m in match_iter:
            syn = m.group(1)
            for key in self.conf_info:
                if syn in self.conf_info[key]:
                    ori = self.conf_info[key][syn]
                    if l == 0:
                        reg = "(?P<%s>%s)" % (re.sub("\d","",syn), ori)
                    else:
                        reg = "(?:%s)" % ori
                    final_reg = re.sub("(?<!\?P)<"+syn+">", reg, final_reg)
                    break
            else:
                #logging.error("no such syntax:%s" % syn)
                return None
        if re.search("(?<!\?P)<(.+?)>", final_reg):
            return self._parse_ori_reg(final_reg, l+1)
        else:
            return final_reg


class Time_Pair():
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.conj_bt = ""
        self.len_line = 0
        self.oriline = ""

    def getOriline(self):
        return self.oriline
    def getStartPos(self):
        return self.time1.pos_s
    def getEndPos(self):
        return self.time2.pos_e

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
        if self.time1.pos_s <= 3:
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



class RawTime(object):
    def __init__(self, year, month, conj=""):
        if type(year)!=unicode or type(month)!=unicode or type(conj)!=unicode:
            print " Time class constructor needs pos(int, Notmust) yea,month,conj(unicode)"
            #logging.error(" Time class constructor needs yea,month,conj(unicode)")
            #logging.error(" year:%s;month:%s;conj:%s;" % (year,month,conj))
        self.pos_s = -1     # essential
        self.year = year    # essential
        self.month = month  # essential
        self.conj = conj    # essential
        self.pos_e = -1
        self.length = 0
        self.year_range = []
        self.month_range = []
        # struct
        self.year = self.year2str()
        self.month = self.month2str()

    def setLen(self, length):
        self.length = length
        if self.pos_s != -1:
            self.pos_e = self.pos_s + self.length - 1

    def setPos(self, pos_start):
        self.pos_s = pos_start
        if self.length != 0:
            self.pos_e = self.pos_s + self.length - 1

    def setRange(self, year_range, month_range):
        self.year_range = year_range
        self.month_range = month_range

    def islegal(self):
        try:
            y = int(self.year)
            m = int(self.month)
        except:
            return False
        if y < self.year_range[0] or y > self.year_range[1]:
            return False
        if m < self.month_range[0] or m > self.month_range[1]:
            return False
        pass
        return True

    def equal(self, tObj):
        if type(tObj) != self.__class__:
            return False
        if tObj.year != self.year or tObj.month != self.month:
            return False
        if tObj.conj != self.conj:
            return False
        if tObj.pos_e != self.pos_e and tObj.pos_s != self.pos_s:
            return False
        pass
        return True

    def toString(self):
        return ""

    def getLength(self):
        if self.length != 0:
            return self.length
        else:
            return len(self.year) + len(self.month) + len(self.conj)

    def month2str(self):
        if len(self.month) == 0:
            return u"01"
        if len(self.month) == 2:
            return self.month
        if len(self.month) == 1:
            return u"0"+self.month

    def year2str(self):
        try:
            y = int(self.year)
        except:
            return ""
        if len(self.year) == 4:
            return self.year
        if len(self.year) == 2:
            if y > 80:
                return u"19"+self.year
            if y >= 0 and y <= 20:
                return u"20"+self.year
        return ""

    def isSofar(self):
        return False

    def __str__(self):
        return '{cname}({str},p={pos})'.format(
            cname = self.__class__.__name__,
            str   = self.toString().replace(u"年",".").replace(u"月",""),
            pos   = self.pos_s,
        )

    def __repr__(self):
        return self.__str__();



class standard_Time(RawTime):
    def __init__(self, year, month, conj=""):
        super(standard_Time, self).__init__(year, month, conj)

    def toString(self):
        return u"%s年%s月" % (self.year, self.month2str())

class re_standard_Time(RawTime):
    def __init__(self, year, month, conj=""):
        super(re_standard_Time, self).__init__(year, month, conj)

    def toString(self):
        return u"%s年%s月" % (self.year, self.month)

class only_year_Time(RawTime):
    def __init__(self, year, month, conj=""):
        super(only_year_Time, self).__init__(year, month, conj)
        self.month = u"01"
        self.conj = u""

    def toString(self):
        return u"%s年" % (self.year)

    def getLength(self):
        if self.length != 0:
            return self.length
        else:
            return len(self.year)

class two_year_Time(RawTime):
    def __init__(self, year, month, conj=""):
        super(two_year_Time, self).__init__(year, month, conj)

    def getLength(self):
        if self.length != 0:
            return self.length
        else:
            return RawTime.getLength(self)-2

    def toString(self):
        return u"%s年%s月" % (self.year2str(), self.month)

class whole_struct_Time(RawTime):
    def __init__(self, year, month, conj=""):
        super(whole_struct_Time, self).__init__(year, month, conj)

    def toString(self):
        return u"%s年%s月" % (self.year, self.month)

class so_far_Time(RawTime):
    def __init__(self, year, month, conj=""):
        super(so_far_Time, self).__init__(year, month, conj)

    def toString(self):
        return "present"

    def islegal(self):
        return True

    def isSofar(self):
        return True
