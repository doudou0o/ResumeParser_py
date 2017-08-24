#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
from itertools import izip

from resume_parser import divideModule
from resume_parser.recognize import match_timestamp
from resume_parser.recognize import match_education
from resume_parser.recognize import match_basic
from resume_parser.recognize import match_region
from resume_parser import resume_struct
from resume_parser.utils import StringUtils

template_name = "_zhilian_t0"

def split_headline_block(filetext):
    """
    rtype: list[[titles], text]
    """
    return divideModule.divideHeadlineBlock(filetext, headlines=Headline_Dict,isOnly=True)

def split_eduexp_block(text):
    def issplit(i, lines):
        if re.search(edu_reg, lines[i]):
            return True
        return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def split_workexp_block(text):
    def issplit(i, lines):
        if re.search(work_reg, lines[i]):
            return True
        else:
            return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def split_project_block(text):
    def issplit(i, lines):
        if re.search(project_reg, lines[i]):
            return True
        else:
            return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def split_language_block(text):
    def issplit(i, lines):
        if match_basic.match_language(re.split(u"：", lines[i])[0]):
            return True
        else:
            return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def split_certificate_block(text):
    def issplit(i, lines):
        if re.search(certi_reg, lines[i]):
            return True
        else:
            return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def split_train_block(text):
    def issplit(i, lines):
        if re.search(train_reg, lines[i]):
            return True
        else:
            return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def split_skill_block(text):
    def issplit(i, lines):
        if re.search(skill_reg, lines[i]) and not lines[i].startswith(u"技能名称"):
            return True
        else:
            return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks


def extract_eduinfo(expblock):
    edu = resume_struct.get_education_struct()
    edu["ori_text"] = expblock

    for line in expblock.split("\n"):
        m = re.search(edu_reg, line)
        if m:
            timestamp = match_timestamp.match_timestamp_by_reg(edu_reg, line)
            edu["school_name"] = m.group("school").strip()
            edu["start_time"], edu["end_time"], edu["so_far"] = StringUtils.transform_timestamp(timestamp)
            edu["degree"] = match_education.match_degree(m.group('degree'), 99)
            edu["discipline_name"] = m.group('discipline').strip()
    return edu

def extract_basicinfo(text):
    basic_info = {}
    basic_info["ori_text_"+str(random.randint(0,1000))] = text

    lines = text.split('\n')

    if lines[0].startswith(u"自我评价"):
        basic_info["self_remark"] = "\n".join(lines[1:])
        return basic_info

    for line_pre, line in izip([""]+lines, lines):

        ## update
        mupdate = re.search(u"简历更新时间(:|：)\s*(?P<t>\d{4}\.\d{2}\.\d{2})",line_pre+line)
        if mupdate:
            basic_info["updated_at"]=mupdate.group("t").replace(".", "-")+" 00:00:00"

        ## name
        mname_id = re.search(u"^ID：", line_pre)
        mname_ph = re.search(u"^手机：", line)
        if mname_id and ("name" not in basic_info or not basic_info["name"]):
            basic_info["name"]=line.strip() if len(StringUtils.get_words(line.strip())) in [2,3,4] else ""
        if mname_ph and ("name" not in basic_info or not basic_info["name"]):
            basic_info["name"]=line_pre.strip() if len(StringUtils.get_words(line_pre.strip())) in [2,3,4] else ""

        ## email phone
        email = match_basic.match_email(line)
        phone = match_basic.match_phone(line)
        m_ph = re.search(u"^手机：(\d+)", re.sub(u"(\(|（).+(\)|）)", "",line).replace(" ",""))
        if email: basic_info["contact_email"] = email
        if m_ph: basic_info["contact_phone"] = m_ph.group(1)
        elif phone and "contact_phone" not in basic_info:
            basic_info["contact_phone"] = phone

        ## gender age birth
        if "U" != match_basic.match_gender(line) and (u"岁" in line or u"经验" in line):
            basic_info["gender"] = match_basic.match_gender(line)
        mage = re.search(u"\d+岁", line)
        if mage: basic_info["age"] = int(mage.group()[:-1])
        mbirth=re.search(u"(?P<y>\d{4})年\s*(?P<m>\d{1,2})月",line)
        if mbirth and mage: 
            month=mbirth.group('m')
            if len(mbirth.group("m"))==1:
                month='0'+month
            basic_info["birth"] = mbirth.group('y')+u'年'+month+u'月'
        ## others
        mtel = re.search(u"家庭电话：(.+)", line)
        if mtel: basic_info["contact_tel"] = mtel.group(1).strip()
        mexp = re.search(u"(\d+)年工作经验", line)
        if mexp: basic_info["work_experience"] = int(mexp.group(1))
        mmary = re.search(u"(已|未)婚|Single|Married", line)
        if mmary:basic_info["marital"] = match_basic.match_marital(mmary.group(0).strip())
        maccount = re.search(u"户口：(.+?)(\||$)", line)
        if maccount:
            basic_info["account_str"] = maccount.group().strip()
            basic_info["account"] = match_region.match_region(maccount.group(1).strip())
        maddress = re.search(u"现居住地：(.+?)(\||$)", line)
        if maddress:
            basic_info["address_str"] = maddress.group().strip()
            basic_info["address"] = match_region.match_region(maddress.group(1).strip())
            basic_info["address_province"]="10"#提醒获取
        id_card=re.search(u"[0-9]{17}[xX0-9]",line)
        if id_card:
            basic_info["card"]=id_card.group(0)
        overseas=re.search(u"有海外工作|Overseas Work",line)
        if overseas:
            basic_info["overseas"]="Y"
    return  basic_info

def extract_contactinfo(text):
    return None

def extract_expectinfo(text):
    def extract_from_double_line(preline, line, r_oneline, r_doubleline, pn):
        m_oneline = re.search(r_oneline, line)
        m_twoline = re.search(r_doubleline, preline)
        if m_oneline or (m_twoline and not re.search(u":|：", line)):
            if m_oneline and len(m_oneline.group(pn).strip())>2:
                return m_oneline.group(pn).strip()
            elif m_twoline:
                return line
        return None

    expectinfo = {}
    for preline,line in izip([""]+text.split("\n"), text.split("\n")):
        mloc = u"^期望工作地区(：|:)(?P<eloc>.+)$"
        mloc_double_line = u"^期望工作地区(：|:)$"
        eloc = extract_from_double_line(preline, line, mloc, mloc_double_line, "eloc")
        if eloc:
            expectinfo["expect_city_names"] = re.sub(u"、", ",", eloc)

        mpos = u"^期望从事职业(：|:)(?P<epos>.+)$"
        mpos_twice_line = u"^期望从事职业(：|:)$"
        epos = extract_from_double_line(preline, line, mpos, mpos_twice_line, "epos")
        if epos:
            expectinfo["expect_position_name"] = re.sub(u"、", ",", epos)

        mindus =  u"^期望从事行业(：|:)(?P<eindus>.+)$"
        mindus2 = u"^期望从事行业(：|:)$"
        eindus = extract_from_double_line(preline, line, mindus, mindus2, "eindus")
        if eindus:
            expectinfo["expect_industry_name"] = re.sub(u"、", ",", eindus)

        msalary = u"^期望月薪(：|:)(?P<esal>.+)$"
        msalary2= u"^期望月薪(：|:)$"
        esal = extract_from_double_line(preline, line, msalary, msalary2, "esal")
        if esal:
            m_monthsal = re.search("(?P<f>\d{3,5})-(?P<t>\d{3,5})", esal)
            if m_monthsal:
                expectinfo["expect_salary_from"] = round(float(m_monthsal.group('f'))/1000.0,1)
                expectinfo["expect_salary_to"] = float(m_monthsal.group('t'))/1000.0
    return expectinfo


def extract_workinfo(text):
    work = resume_struct.get_emplyment_struct()
    work["ori_text"] = text
    lastline = "not found company"
    for line in text.split('\n'):
        if lastline == "not found company":
            m_company = re.search(work_reg, line)
            if m_company:
                timestamp = match_timestamp.match_timestamp_by_reg(work_reg, line)
                work["corporation_name"] = clean_company_name(m_company.group("company"))
                work["start_time"], work["end_time"], work["so_far"] = StringUtils.transform_timestamp(timestamp)
                lastline = "company name"
            pass
        elif lastline == "company name":
            items = line.split("|")
            if len(items)==3:
                work["architecture_name"] =items[0].strip()
                work["position_name"] =items[1].strip()
                lastline = "position"
            if len(items)==2:
                work["position_name"] =items[0].strip()
                lastline = "position"
        elif lastline == "position":
            items = line.split("|")
            if len(items) > 1:
                work["industry_name"] = items[0]
                work["corporation_type"]=re.sub(u"企业性质(:|：)","",items[1])
            lastline = "industry"
        elif lastline == "industry":
            work["responsibilities"] += '\n'+line if work["responsibilities"] else line
    pass
    work["responsibilities"] = re.sub(u"^工作描述(:|：)", "",  work["responsibilities"]).strip()
    return work

def clean_company_name(c_name):
    c_name_ori = c_name
    c_name = re.sub(u"^(:|：)","",c_name)
    c_name = re.sub(u"[（）\(\)\[\]]$","",c_name)
    c_name = re.sub(u"\d+\s*(年|个月)$","",c_name)
    c_name = re.sub(u"\d+$","",c_name)
    c_name = re.sub(u"\d+-\d+人.*","",c_name)
    c_name = re.sub(u"少于\d+人.*","",c_name)
    c_name = c_name.strip()
    if c_name == c_name_ori: return c_name
    else:
        return clean_company_name(c_name)


def extract_projectinfo(text):
    project = resume_struct.get_project_struct()
    project["ori_text"] = text
    lines = text.split("\n")

    isDesc, isResp = False, False
    for preline, line in izip([""]+lines, lines):
        m_proj = re.search(project_reg, line)
        if m_proj:
            timestamp = match_timestamp.match_timestamp_by_reg(project_reg, line)
            project["name"] = m_proj.group("project").strip()
            project["start_time"], project["end_time"], project["so_far"] = StringUtils.transform_timestamp(timestamp)

        m_desc = re.search(u"项目描述(:|：)", line)
        if m_desc:
            line = re.sub(u"项目描述(:|：)","", line).strip()
            isDesc, isResp = True, False
        m_resp = re.search(u"责任描述(:|：)", line)
        if m_resp:
            line = re.sub(u"责任描述(:|：)","", line).strip()
            isDesc, isResp = False, True
        pass
        if isDesc:project["describe"] += '\n'+line if project["describe"] and line else line
        if isResp:project["responsibilities"] += '\n'+line if project["responsibilities"] and line else line
    return project

def extract_languageinfo(text):
    lang = resume_struct.get_language_struct()
    lines = text.split('\n')
    for line_pre, line in izip([""]+lines, lines):
        ans = match_basic.match_language(line_pre)
        # 语言和等级分两行的情况
        if ans:
            lang["name"] = ans.strip()
            lang["level"] = line.strip()
        # 语言和等级在一行的情况
        else:
            items = filter(lambda x: len(x)>1 , re.split(u"：|:", line))
            if len(items)==2 and match_basic.match_language(items[0]):
                lang["name"] = items[0]
                lang["level"] = items[1]
        pass
    return lang

def extract_certinfo(text):
    cert = resume_struct.get_certificate_struct()

    for line in text.split('\n'):
        m_cert = re.search(certi_reg, line)
        if m_cert:
            timestamp = match_timestamp.match_timestamp_by_reg(certi_reg, line)
            cert["name"] = m_cert.group("name").strip()
            cert["start_time"], _,_ = StringUtils.transform_timestamp(timestamp)

    return cert

def extract_traininfo(text):
    train = resume_struct.get_training_struct()
    isDesc=False
    for line in text.split('\n'):
        m_train = re.search(train_reg, line)
        if m_train:
            timestamp = match_timestamp.match_timestamp_by_reg(train_reg, line)
            train["name"] = m_train.group("train").strip()
            train["start_time"], train["end_time"], train["so_far"] = StringUtils.transform_timestamp(timestamp)
        mauth = re.search(u"^培训机构：(.+)", line)
        if mauth:
            train["authority"] = mauth.group(1).strip()
        mcity = re.search(u"^培训地点：(.+)", line)
        if mcity:
            train["city"] = mcity.group(1).strip()
        mdesc = re.search(u"^培训描述：(.+)", line)
        if mdesc and not isDesc :
            train["description"] = mdesc.group(1).strip()
            isDesc=True
        elif isDesc:
            train["description"]=train["description"]+line
    return train

def extract_skillinfo(text):
    skill = resume_struct.get_skill_struct()

    for line in text.split("\n"):
        m_skill = re.search(skill_reg, line)
        if m_skill:
            skill["name"] = m_skill.group("n").strip()
            skill["level"] = m_skill.group("l").strip()
    return skill



###### zhilian_0 template config
# zhilian headlines
Headline_Dict={}
Headline_Dict[u"个人信息"] =  0
Headline_Dict[u"求职意向"] =  2
Headline_Dict[u"教育经历"] =  5
Headline_Dict[u"工作经历"] =  4
Headline_Dict[u"项目经历"] =  6
Headline_Dict[u"语言能力"] =  8
Headline_Dict[u"培训经历"] =  9
Headline_Dict[u"专业技能"] = 10
Headline_Dict[u"语言"]     =  8
Headline_Dict[u"证书"]     =  7

Headline_Dict[u"所获奖项"] = 99
Headline_Dict[u"在校学习情况"] = 99
Headline_Dict[u"在校实践经历"] = 99
Headline_Dict[u"最近工作"] = 99
Headline_Dict[u"自我评价"] = 99
Headline_Dict[u"社会经验"] = 99
Headline_Dict[u"校内职务"] = 99
Headline_Dict[u"其他信息"] = 99
Headline_Dict[u"IT技能"]   = 99
Headline_Dict[u"兴趣爱好"]   = 99
Headline_Dict[u"附件"]     = 99
Headline_Dict[u"著作"]     = 99
Headline_Dict[u"附件简历"]     = 99
Headline_Dict[u"特殊技能"]     = 99
Headline_Dict[u"宗教信仰"]     = 99
Headline_Dict[u"其他信息"]     = 99

# zhilian edu config
edu_reg = u"(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s*-\s*(((?P<ey>\d{4})\.(?P<em>\d{1,2}))|(?P<ep>至今))\s+(?P<school>.+?)\s+(?P<discipline>.+?)\s+(?P<degree>.+)"

# zhilian work config
work_reg = u"^(?P<sy>\d{4}).(?P<sm>\d{1,2})\s*-\s*((?P<ey>\d{4}).(?P<em>\d{1,2})|(?P<ep>至今))\s*(?P<company>.+?)(\d+年|\d+个月|$)"

# zhilian project config
project_reg = u"^(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s*-\s*((?P<ey>\d{4})\.(?P<em>\d{1,2})|(?P<ep>至今))\s*(?P<project>.+)"

certi_reg = u"^(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s+(?P<name>.+)"

train_reg = u"^(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s*-\s*((?P<ey>\d{4})\.(?P<em>\d{1,2})|(?P<ep>至今))\s+(?P<train>.+)"

skill_reg = u"(?P<n>.+?)(:|：)(?P<l>.+)"

