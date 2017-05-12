#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import ConfigParser
import re
import TimeBuilderFactory
from TimeBuilderFactory import Time_Pair
import os


dirpath  = os.path.dirname(__file__)
timeconf = os.path.join(dirpath, 'timeBNF.conf')


class TimeMatcher():
    """ TimeMatcher get a string line and return a pair of time interval
    """
    def __init__(self):
        self.priority_TimeName_list = []
        self.conf = ConfigParser.ConfigParser()
        self.readConf(timeconf)
        self.init()

    def init(self):
        self.onlylefttime_cands = []

    def getTimePairList(self, TimeNameSet, sofarList, line):
        time_pair_list = []
        for tName in TimeNameSet:
            TB = TimeBuilderFactory.getTB(tName)
            #logging.debug(tName)
            if TB == None:continue;
            tObj_list = TB.findall(line)
            t_pair_list = []
            if len(tObj_list) + (1 if sofarList else 0) > 1:
                tObj_list.extend(sofarList)
                t_pair_list = self._make_pair(tObj_list, line)
            if len(t_pair_list)==0 and len(tObj_list) > 0:
                self._make_pair_onlylefttime(tObj_list, line)
            if len(t_pair_list) > 0:
                time_pair_list.extend(t_pair_list)
        return time_pair_list


    def match_time(self, line):
        TB = TimeBuilderFactory.getTB("so_far_Time")
        sofarList = TB.findall(line)

        for TimeNameSet in self.priority_TimeName_list:
            time_pair_list = self.getTimePairList(TimeNameSet, sofarList, line)
            if len(time_pair_list) > 0:
                time_pair_list = self._sort_pair(time_pair_list)
                t_pair = time_pair_list[0]
                return t_pair.toString(), t_pair
        return None, None

    def match_time_reg(self, line):
        return None, None

    def match_time_onlyLeft(self, line):
        for lefttime in self.onlylefttime_cands:
            prefix = line[:lefttime.time1.pos_s]
            suffix = line[lefttime.time1.pos_e+1] if lefttime.time1.pos_e+1 < len(line) else ""
            if lefttime.time1.__class__.__name__ not in ["standard_Time","whole_struct_Time"]:
                continue
            if re.search(u"[0-9\u4e00-\u9fa5]", prefix):
                continue
            if re.search(u"[0-9]", suffix):
                continue
            #if len(re.sub("[\-0-9]","",line[lefttime.time1.pos_e+1:]))<2:
            #    return
            return lefttime.toString().replace("present", "  "), lefttime
        return None, None

    def extractTimeStamp(self, line):
        self.init()
        line = Handle_helper().handle(line)

        TimeStamp = self.match_time(line)
        if TimeStamp[0] is not None:
            return TimeStamp

        TimeStamp = self.match_time_reg(line)
        if TimeStamp[0] is not None:
            return TimeStamp

        TimeStamp = self.match_time_onlyLeft(line)
        if TimeStamp[0] is not None:
            return TimeStamp

        return None,None


    def readConf(self, conf_file):
        ans = self.conf.read(conf_file)
        if not ans:
            #logging.error("not found conf_file:%s" % conf_file)
            return
        self.priority_TimeName_list = self._get_priority_list()

    def _get_priority_list(self):
        section_name = "time_level"
        if section_name not in self.conf.sections():
            #logging.error("not found time_level section in conf")
            return None
        priority_list = []
        for level in self.conf.options(section_name):
            classNames = self.conf.get(section_name, level)
            classNameSet = map(lambda x: x.strip(), classNames.split(","))
            priority_list.append(classNameSet)
        #logging.debug("got time_level sections:"+ str(priority_list))
        return priority_list

    def _make_pair(self, tObj_list, line):
        result_pair = []
        if not tObj_list or len(tObj_list) < 2:
            return []
        for i in range(len(tObj_list)):
            for j in range(i+1, len(tObj_list)):
                tObj_1 = tObj_list[i]
                tObj_2 = tObj_list[j]
                t_pair = Time_Pair(tObj_1, tObj_2)
                t_pair.setline(line)
                if t_pair.islegal():
                    result_pair.append(t_pair)
        return result_pair

    def _make_pair_onlylefttime(self, tObj_list, line):
        result_pair = []
        for tObj in tObj_list:
            if tObj.pos_s <= 1:
                tObj2 = TimeBuilderFactory.getTB("so_far_Time").findall("present")[0]
                self.onlylefttime_cands.append(Time_Pair(tObj, tObj2))
                result_pair.append(Time_Pair(tObj, tObj2))
        return result_pair

    def _sort_pair(self, t_pair_list):
        #logging.debug( "-- candidates --")
        for t_p in t_pair_list:
            pass
            #logging.debug( t_p.toString() )
        #logging.debug( "--return sort--")
        return t_pair_list



class Handle_helper():
    def handle_chinese(self, line):
        """transform number of chinese"""
        ChMap={u'一':'1',u'二':'2',u'三':'3',u'四':'4',u'五':'5',u'六':'6',u'七':'7',u'八':'8',u'九':'9',u'零':'0'}
        for ch in ChMap:
            line = re.sub(ch,ChMap[ch],line)
        if re.search(u'十', line):
            match = re.search(u'(\d?)十(\d?)', line)
            if match.group(1):
                num = int(match.group(1))*10
            else:
                num = 10
            if match.group(2):
                num += int(match.group(2))
            line = re.sub(u'(\d?)十(\d?)', str(num), line)

        return line

    def handle_english(self, line):
        """transform month words of English"""
        monthEn={'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
        monthAbb={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','July':'07','Aug':'08','Sept':'09','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        for m in [x for x in monthEn if x in line]:
            line = re.sub(u'(?P<m>\\b'+m+'(.)?)(\s{0,3})(?P<y>\\d{4})','\g<y>.\g<m>',line)
            line = re.sub(u'\\b'+m+'((\.)?)',monthEn[m],line)
        for m in [x for x in monthAbb if x in line]:
            line = re.sub(u'(?P<m>\\b'+m+'(.)?)(\s{0,3})(?P<y>\\d{4})','\g<y>.\g<m>',line)
            line = re.sub(u'\\b'+m+'((\.)?)',monthAbb[m],line)

        return line

    def strQ2B(self, ustring):
        """把字符串全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code==0x3000:
                inside_code=0x0020
            else:
                inside_code-=0xfee0
            if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                rstring += uchar
            else:
                rstring += unichr(inside_code)
        return rstring

    def removeBlank(self, line):
        """ do not remove the blank that chars between blank are both number or eng"""
        line = line.strip()
        line = re.sub("\s+"," ",line)
        oriline = line
        length = len(line)
        for i,ch in enumerate(line[::-1]):
            if ch == " ":
                a = line[length-i-1-1]
                b = line[length-i-1+1]
                if re.search("\d",a) and re.search("\d", b):
                    continue
                if re.search("[a-zA-Z]",a) and re.search("[a-zA-Z]", b):
                    continue
                j = length - i - 1
                oriline = oriline[:j] + oriline[j+1:]
        return oriline

    def removeLongNum(self, line):
        return re.sub("\d{5,}","xx",line)

    def removeDay(self, line):
        return re.sub(u"(\d+月)\d+日", "\g<1>", line)

    def handle(self, line):
        line = self.strQ2B(line)
        line = self.handle_chinese(line)
        line = self.handle_english(line)
        line = self.removeBlank(line)
        line = self.removeLongNum(line)
        line = self.removeDay(line)
        line = re.sub("-+","-",line)
        return line



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format="%(asctime)s %(filename)s %(funcName)s[line:%(lineno)d] %(levelname)s %(message)s",)

    tm = TimeMatcher()

    #print tm.extractTimeStamp(u"May 2006 – Sep. 2008")
    print tm.extractTimeStamp(u"Oct. 2008 – Aug . 2011")
    #exit()
    print tm.extractTimeStamp(u"12-09-01-16")
    print tm.extractTimeStamp(u"1979/12/29")
    print tm.extractTimeStamp(u"2004.09至今")
    print tm.extractTimeStamp(u"2006.9---至今")
    print tm.extractTimeStamp(u"一.    1997年9月--2001年7月")
    print tm.extractTimeStamp(u"07-1992-1998.021k")
    print tm.extractTimeStamp(u"01-1992.09-1998.021k")
    print tm.extractTimeStamp(u"2.05/92 -08/02hahahaha")
    print tm.extractTimeStamp(u"April.2009 - July.2010")
    print tm.extractTimeStamp(u"2009 - 2010")
    print tm.extractTimeStamp(u"1979/12/29--1999/12/29")
