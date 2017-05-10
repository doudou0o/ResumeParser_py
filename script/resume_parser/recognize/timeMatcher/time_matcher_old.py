#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import os
import time
import copy
reload(sys)
sys.setdefaultencoding('utf-8')
'''
前提：时间区间在一行中
输出：匹配到的时间区间、此行内容、行号
'''
def strQ2B(ustring):
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

class time_matcher():
    def __init__(self,fn,fc):
        self.filename=fn
        self.filecontent=fc
        self.ori_lines=[]
        self.timelines=[]
        self.timeformatlines=[]
        self.dict_lines_format={} # key:format_lines, value: timelines

        self.final_time_match=[]# 行号，行内容，时间内容1991.02-1992.02
        pass

    def year_filter(self,line):
        line = re.sub(' ','',line)
        line = line.decode('utf8')
        line = strQ2B(line)
        pattern = re.compile(u'(\\d{4,})|([一|二|三|四|五|六|七|八|九|零]{4,})')
        match_info = re.search(pattern,line)
        if match_info:
            if len(match_info.group()) >4:
                return '-1'
            return line.encode('utf8')
        else:
            return '-1'
        pass

    def isyear(self,line):
        if line.isdigit():
            try:
                y = int(line)
            except:
                return False
            if y<1900 or y>2500:
                return False
        return True

    def ismonth(self,line):
        if line.isdigit():
            try:
                m = int(line)
            except:
                return False
            if m<1 or m>12:
                return False
            return True
        else:
            monthCn = '一二三四五六七八九十'.decode('utf8')
            monthMap={monthCn[0]:1,monthCn[1]:2,monthCn[2]:3,monthCn[3]:4,monthCn[4]:5,monthCn[5]:6,monthCn[6]:7,monthCn[7]:8,monthCn[8]:9,monthCn[9]:10}
            if len(line)==2 and line.startswith('十'.encode('utf8')):
                if line[1]=='一' or line[1]=='二':
                    return True
                else:
                    return False
            elif len(line)==1:
                if line in monthMap:
                    return True
            else:
                return False

    def month_filter(self,line):
        line = re.sub(' ','',line)
        line = line.decode('utf8')
        line = strQ2B(line)
        conj = u'[\.|/|,|\-|年]'
        cn_num = u'[一|二|三|四|五|六|七|八|九|零]'
        pattern = re.compile(u'(\\d{4}'+conj+'(?P<m1>\\d{1,2}))|('+cn_num+'{4}'+conj+'(?P<m2>(十)?'+cn_num+'))')
        match_info = re.search(pattern,line)
        if match_info:
            if match_info.group('m1'):
                if self.ismonth(match_info.group('m1')):
                    return line.encode('utf8')
            elif match_info.group('m2'):
                if self.ismonth(match_info.group('m2')):
                    return line.encode('utf8')
        #2000-2010纯年
        match_dy = re.search(u'(?P<y1>\\d{4})((年)?)[\.|-|--|~](?P<y2>\\d{4})((年)?)',line)
        if match_dy:
            if self.isyear(match_dy.group('y1')) and self.isyear(match_dy.group('y2')):
                return line.encode('utf8')
        #last chance
        line = self.format_time(line)
        if re.search('\\d{4}\.\\d{2}',line):
            return line.encode('utf8')
        else:
            return '-1'
        pass

    def addpoint(self,matched):
        Y = matched.group('y')
        M = matched.group('m')
        if not self.ismonth(M):
            return matched.group()
        if not self.isyear(Y):
            return matched.group()
        return Y+'.'+M

    def addzero(self,matched):
        if len(matched.group('m')) == 1:
            if self.isyear(matched.group('y')):
                return matched.group(1)[:5]+'0'+matched.group(1)[5:]
        return matched.group(1)

    def format_time(self,line):
        line = line.decode('utf8')
        line = strQ2B(line)

        monthMap={'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'零':0}
        for m in monthMap:
            line = line.replace(m,str(monthMap[m]))

        monthEn={'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
        monthAbb={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','July':'07','Aug':'08','Sept':'09','Oct':'10','Nov':'11','Dec':'12'}
        for m in [x for x in monthEn if x in line]:
            line = re.sub(u'(?P<m>\\b'+m+'(.)?)(\s{0,3})(?P<y>\\d{4})','\g<y>.\g<m>',line)
            line = re.sub(u'\\b'+m+'((\.)?)',monthEn[m],line)
        for m in [x for x in monthAbb if x in line]:
            line = re.sub(u'(?P<m>\\b'+m+'(.)?)(\s{0,3})(?P<y>\\d{4})','\g<y>.\g<m>',line)
            line = re.sub(u'\\b'+m+'((\.)?)',monthAbb[m],line)

        line = re.sub(' ','',line)
        line = re.sub(u'(\\d{4})年(\\d{1,2})月((\\d{1,2})日)?','\g<1>.\g<2>',line)
        line = re.sub(u'(?P<y>\\d{4}).(?P<m>\\d{1,2})',self.addpoint,line)
        line = re.sub(u'((?P<y>\\d{4})\.(?P<m>\\d{1,2}))',self.addzero,line)
        line = re.sub(u'(\\d{4}\.\\d{2})月','\g<1>',line)
        line = re.sub(u'(?i)(present)|(now)|(current)|(至今)|(目前)|今|(现在)','present',line)
        return line

    def timeInterval_filter(self,line):
        line = re.sub(' ','',line)
        line = re.sub('\t','',line)
        line = line.decode('utf8')
        line = strQ2B(line)
        pattern = re.compile('(?P<T1>\\d{4}\.\\d{2}).{,5}(?P<T2>(\\d{4}\.\\d{2})|(present))')
        match_info = re.search(pattern,line)
        if match_info:
            atime = match_info.group('T1')
            if match_info.group('T2') == 'present':
                btime = time.strftime("%Y.%m", time.localtime())
            else:
                btime = match_info.group('T2')

            if not (self.isyear(atime[:4]) and self.ismonth(atime[5:]) and self.isyear(btime[:4]) and self.ismonth(btime[5:])):
                return '-1'
            a_struct_time = time.strptime(atime,'%Y.%m')
            b_struct_time = time.strptime(btime,'%Y.%m')
            if a_struct_time <= b_struct_time:
                return atime+'-'+match_info.group('T2')
            else:
                return '-1'
        else:
            ans = self.BeginofLine(line)
            if ans != -1:
                return ans
            return '-1'
        pass

    def content_filter(self,line):
        #TODO
        pass

    def save(self):
        content = '\n'.join(self.timeformatlines)
        with open('format.txt', 'a') as f:
            f.write(content)

        content = '\n'.join(self.timelines)
        with open('filter.txt', 'a') as f:
            f.write(content)

    def build_final_time_match(self):
        for i,finalline in enumerate(self.timeformatlines):
            if finalline == '-1':
                continue
            ori_line = self.timelines[i]
            no_line = i
            result1 = re.search('(\\d{4}\.\\d{2}).{1,3}((\\d{4}\.\\d{2})|(present))',finalline)
            reg1 = re.search("^\d{4}.\d{1,2}-",finalline)
            reg2 = re.search("^\d{4}-\d{4}",finalline)

            if result1:
                matched_time = result1.group()
                matched_time = re.sub("(\d{4}\.\d{2}).{1,3}((\\d{4}\.\\d{2})|(present))","\g<1>-\g<2>",matched_time)
                matched_time = re.sub("(\d{4})\.(\d{2})",u"\g<1>年\g<2>月",matched_time)
            elif reg1:
                matched_time = reg1.group()
                matched_time = re.sub("(\d{4}).(\d{1,2})",u"\g<1>年\g<2>月",matched_time)
            elif reg2:
                matched_time = reg2.group()
                matched_time = re.sub("\d{4}",u"\g<0>年",matched_time)
            
            self.final_time_match.append({'line_no':no_line,'line_content':ori_line,'matched_time':matched_time})

    def run(self):
        self.ori_lines = ''.join(self.filecontent).split('\n')
        self.timelines = copy.copy(self.ori_lines)
        self.timelines = map(self.year_filter,self.timelines)
        self.timelines = map(self.month_filter,self.timelines)
        self.timeformatlines = map(self.format_time,self.timelines)
        self.timeformatlines = map(self.timeInterval_filter,self.timeformatlines)

#        self.timeformatlines = filter(self.content_filter,self.timeformatlines)
#        self.save()
        self.build_final_time_match()
        pass

    def find_only_years(self,line):
        line = re.sub(' ','',line)
        line = re.sub('\t','',line)
        line = line.decode('utf8')
        pattern = re.compile('(?P<T1>\\d{4}).{,3}(?P<T2>(\\d{4}))')
        match_info = re.search(pattern,line)
        if match_info:
            T1 = match_info.group('T1')
            T2 = match_info.group('T2')
            return T1+'-'+T2
        return ''

    def BeginofLine(self, line):
        line = re.sub('\s+-+\s+','-',line)
        line = re.sub(u'至|到|~','-',line)
        line = ChineseNumer(line)
        reg1 = re.search("^\d{4}.\d{1,2}-",line)
        reg2 = re.search("^\d{4}-\d{4}",line)
        reg3 = re.search("^(\d{4}.\d{1,2}).\d{1,2}-",line)
        if reg1:
            return reg1.group()
        elif reg2:
            return reg2.group()
        elif reg3:
            return reg3.group(1)+'-'
        else:
            return -1

def ChineseNumer(line):
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


