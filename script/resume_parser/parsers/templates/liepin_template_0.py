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

template_name = "_liepin_t0"

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
        if match_basic.match_language(re.split("\s+", lines[i])[0]):
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

    time_found = False
    for line in expblock.split("\n"):
        m_time = re.search(edu_reg, line)
        if m_time:
            timestamp = match_timestamp.match_timestamp_by_reg(edu_reg, line)
            edu["start_time"], edu["end_time"], edu["so_far"] = StringUtils.transform_timestamp(timestamp)
            time_found = True
            continue
        if time_found:
            edu["school_name"] = line.strip()
            time_found = False
        m_dis = re.search(u"专业(:|：)(?P<dis>.+)", line)
        if m_dis:
            edu["discipline_name"] = m_dis.group("dis").strip()
        m_deg = re.search(u"学历(:|：)(?P<deg>.+)", line)
        if m_deg:
            edu["degree"] = match_education.match_degree(m_deg.group("deg").strip())
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
        m_update = re.search(u"最近登录：\s*(?P<up>\d{4}-\d{2}-\d{2})", line)
        if m_update:
            basic_info["updated_at"] = m_update.group("up")+" 00:00:00"

        ## name
        m_name = re.search(u"姓名(:|：)\s*(?P<n>.+?)\s+", line)
        if m_name:
            basic_info["name"] = m_name.group("n")

        ## email phone
        email = match_basic.match_email(line)
        phone = match_basic.match_phone(line)
        if email: basic_info["contact_email"] = email
        if phone: basic_info["contact_phone"] = phone

        ## gender
        if "U" != match_basic.match_gender(line) and re.search(u"性\s*别" ,line):
            basic_info["gender"] = match_basic.match_gender(line)

        ## age
        mage = re.search(u"年\s*龄(:|：)\s*(?P<age>\d+)", line)
        if mage: basic_info["age"] = int(mage.group("age"))

        ## others
        maddress = re.search(u"工作地点(:|：)(?P<a>.+)$", line)
        if maddress:
            basic_info["address_str"] = maddress.group("a").strip()
            basic_info["address"] = match_region.match_region(maddress.group("a").strip())
        mexper = re.search(u"工作年限(:|：)\s*(?P<n>\d)\s*年", line)
        if mexper:
            basic_info["work_experience"] = int(mexper.group("n"))
        maccount = re.search(u"户籍(:|：)\s*(?P<a>.+)", line)
        if maccount:
            basic_info["account"] = match_region.match_region(maccount.group("a").strip())

    return  basic_info

def extract_contactinfo(text):
    contact_info = {}

    phone = match_basic.match_phone(text)
    email = match_basic.match_email(text)
    if phone: contact_info["phone"] = phone
    if email: contact_info["email"] = phone

    for line in text.split('\n'):
        mtel = re.search(u"家庭电话：(.+)", line)
        if mtel: contact_info["contact_tel"] = mtel.group(1)
    pass
    return contact_info

def extract_expectinfo(text):
    expectinfo = {}
    for line in text.split("\n"):
        mloc = re.search(u"期望工作地点：(.+)$", line)
        if mloc:
            expectinfo["expect_city_names"] = re.sub(u";", ",", mloc.group(1).strip()).strip()
        mpos = re.search(u"期望从事职业：(.+)$", line)
        if mpos:
            expectinfo["expect_position_name"] = re.sub(u";", ",", mpos.group(1).strip()).strip()
        mindus = re.search(u"期望从事行业：(.+)$", line)
        if mindus:
            expectinfo["expect_industry_name"] = re.sub(u";", ",", mindus.group(1).strip()).strip()
        msalary = re.search(u"^期望薪资：(.+)$", line)
        if msalary:
            expectsalary = msalary.group(1).strip()
            m_monthsal = re.search("(?P<f>\d{3,5})-(?P<t>\d{3,5})", expectsalary)
            if m_monthsal:
                expectinfo["expect_salary_from"] = float(m_monthsal.group('f'))/1000.0
                expectinfo["expect_salary_to"] = float(m_monthsal.group('t'))/1000.0
        m_yearsalary = re.search(u"^期望年薪：\s*(\d+\.\d+)万", line)
        if m_yearsalary:
            expectsalary = m_yearsalary.group(1).strip()
            expectinfo["expect_annual_salary_from"] = float(expectsalary)*10.0
            expectinfo["expect_annual_salary_to"] = float(expectsalary)*10.0

    return expectinfo


def extract_workinfo(text):
    work = resume_struct.get_emplyment_struct()
    work["ori_text"] = text

    last_line, isResp = "", False
    for line in text.split('\n'):
        m_time = re.search(work_reg, line)
        if m_time:
            timestamp = match_timestamp.match_timestamp_by_reg(work_reg, line)
            work["start_time"], work["end_time"], work["so_far"] = StringUtils.transform_timestamp(timestamp)
            last_line = "time"; continue
        if last_line == "time":
            work["corporation_name"] = line
            last_line = "corp_name"; continue
        if last_line == "corp_name":
            work["position_name"] = line; last_line=""; continue

        m_loc = re.search(u"所在地区(：|:)(?P<loc>.+)", line)
        if m_loc:
            work["city"] = m_loc.group("loc")

        m_resp = re.search(u"职责业绩(：|:)", line)
        if m_resp:
            line = re.sub(u".*职责业绩(：|:)", "", line)
            isResp = True

        if isResp: work["responsibilities"] += "\n"+line if work["responsibilities"] and line else line
    pass
    work["responsibilities"] = re.sub(u"^工作描述(:|：)", "",  work["responsibilities"]).strip()
    return work

def clean_company_name(c_name):
    c_name_ori = c_name
    c_name = re.sub(u"^(:|：)","",c_name)
    c_name = re.sub(u"[（）\(\)\[\]]$","",c_name)
    c_name = re.sub(u"\d+\s*(年|个月)$","",c_name)
    c_name = re.sub(u"\d+$","",c_name)
    c_name = re.sub(u"\d+-\d+人.+","",c_name)
    c_name = c_name.strip()
    if c_name == c_name_ori: return c_name
    else:
        return clean_company_name(c_name)



def extract_projectinfo(text):
    project = resume_struct.get_project_struct()
    project["ori_text"] = text

    time_found = False
    isResp, isDesc, isAchi = False,False,False
    for line in text.split('\n'):
        m_proj = re.search(project_reg, line)
        if m_proj:
            timestamp = match_timestamp.match_timestamp_by_reg(project_reg, line)
            project["start_time"], project["end_time"], project["so_far"] = StringUtils.transform_timestamp(timestamp)
            time_found = True;continue
        if time_found:
            project["name"], time_found = line, False
            continue

        m_posi = re.search(u"项目职务(:|：)\s*(?P<posi>.+)", line)
        if m_posi:
            project["position_name"] = m_posi.group("posi")
        m_corp = re.search(u"所在公司(:|：)(?P<corp>.+)", line)
        if m_corp:
            project["corporation_name"] = m_corp.group("corp")
        m_desc = re.search(u"项目简介(:|：)", line)
        if m_desc:
            line = re.sub(u"项目简介(:|：)","", line).strip()
            isResp, isDesc, isAchi = False,True,False
        m_resp = re.search(u"项目职责(:|：)", line)
        if m_resp:
            line = re.sub(u"项目职责(:|：)","", line).strip()
            isResp, isDesc, isAchi = True,False,False
        m_achi = re.search(u"项目业绩(:|：)", line)
        if m_achi:
            line = re.sub(u"项目业绩(:|：)","", line).strip()
            isResp, isDesc, isAchi = False,False,True
        pass
        if isDesc: project["describe"] += '\n'+line if project["describe"] and line else line
        if isResp: project["responsibilities"] += '\n'+line if project["responsibilities"] and line else line
        if isAchi: project["achivement"] += "\n"+line if project["achivement"] and line else line
    pass
    return project

def extract_languageinfo(text):
    lang = resume_struct.get_language_struct()
    return lang

def extract_certinfo(text):
    cert = resume_struct.get_certificate_struct()
    return cert

def extract_traininfo(text):
    train = resume_struct.get_training_struct()
    return train

def extract_skillinfo(text):
    skill = resume_struct.get_skill_struct()
    return skill



###### liepin_0 template config
# liepin headlines
Headline_Dict={}
Headline_Dict[u"个人信息"] =  0
Headline_Dict[u"求职意向"] =  2
Headline_Dict[u"教育经历"] =  5
Headline_Dict[u"工作经历"] =  4
Headline_Dict[u"项目经历"] =  6

Headline_Dict[u"语言能力"] =  8
Headline_Dict[u"培训经历"] =  9
Headline_Dict[u"在校情况"] = 99
Headline_Dict[u"自我评价"] = 99
Headline_Dict[u"其他信息"] = 99
Headline_Dict[u"附加信息"] = 99

# liepin edu config
edu_reg = u"(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s*-{1,2}\s*(((?P<ey>\d{4})\.(?P<em>\d{1,2}))|(?P<ep>至今))\s*$"

# 51job work config
work_reg = u"^(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s*-{1,2}\s*((?P<ey>\d{4})\.(?P<em>\d{1,2})|(?P<ep>至今))\s*$"

# 51job project config
project_reg = u"^(?P<sy>\d{4})\.(?P<sm>\d{1,2})\s*-{1,2}\s*((?P<ey>\d{4})\.(?P<em>\d{1,2})|(?P<ep>至今))\s*$"

certi_reg = u"--------"

train_reg = u"--------"

skill_reg = u"--------"
