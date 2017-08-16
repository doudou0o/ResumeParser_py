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

template_name = "_51job_t1"

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

    for line in expblock.split("\n"):
        m = re.search(edu_reg, line)
        if m:
            edu["school_name"] = m.group("school").strip()
            edu["discipline_name"] = m.group("disc").strip()
            edu["degree"] = match_education.match_degree(m.group("degree").strip(), 99)
            timestamp = match_timestamp.match_timestamp_by_reg(edu_reg, line)
            edu["start_time"], edu["end_time"], edu["so_far"] = StringUtils.transform_timestamp(timestamp)
        else:
            edu["discipline_desc"] += "\n"+line.strip() if edu["discipline_desc"] else line.strip()

    edu["discipline_desc"] =  re.sub(u"^专业描述(：|:)", "", edu["discipline_desc"]).strip()
    return edu

def extract_basicinfo(text):
    basic_info = {}
    basic_info["ori_text_"+str(random.randint(0,1000))] = text

    lines = text.split('\n')
    if lines[0].startswith(u"自我评价"):
        basic_info["self_remark"] = "\n".join(lines[1:])
        return basic_info

    for line_pre, line in izip([""]+lines, lines):
        ## name update
        m_update = re.search(u"更新时间：\s*(?P<up>\d{4}-\d{2}-\d{2})", line)
        if m_update:
            basic_info["updated_at"] = m_update.group("up")+" 00:00:00"
        if len(line.split("|"))==3:
            if len(StringUtils.get_words(line_pre.strip())) in [2,3,4]:
                basic_info["name"] = line_pre.strip()

        ## email phone
        email = match_basic.match_email(line)
        phone = match_basic.match_phone(line)
        if email: basic_info["contact_email"] = email
        if phone: basic_info["contact_phone"] = phone
        ## gender age birth
        if "U" != match_basic.match_gender(line) and (u"岁" in line or u"经验" in line):
            basic_info["gender"] = match_basic.match_gender(line)
        mage = re.search(u"\d+岁", line)
        if mage: basic_info["age"] = int(mage.group()[:-1])
        mbirth = re.search(u"\d{4}年\s?\d{1,2}月\s?\d{1,2}日", line)
        if mbirth and mage: basic_info["birth"] = mbirth.group().replace(" ", "")
        ## others
        mtel = re.search(u"家庭电话：(.+)", line)
        if mtel: basic_info["contact_tel"] = mtel.group(1).strip()
        mexp = re.search(u"(\d+)年工作经验", line)
        if mexp: basic_info["work_experience"] = int(mexp.group(1))
        mmary = re.search(u"婚姻状况：(.+)", line)
        if mmary:basic_info["marital"] = match_basic.match_marital(mmary.group(1).strip())
        maccount = re.search(u"户口/国籍：(.+)", line)
        if maccount:
            basic_info["account_str"] = maccount.group(1).strip()
            basic_info["account"] = match_region.match_region(maccount.group(1).strip())
        maddress = re.search(u"现居住?(.+?)(\||$)", line)
        if maddress:
            basic_info["address_str"] = maddress.group(1).strip()
            basic_info["address"] = match_region.match_region(maddress.group(1).strip())

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
    selfremark = False
    for line in text.split("\n"):
        mloc = re.search(u"地点：(.+)$", line)
        if mloc:
            expectinfo["expect_city_names"] = re.sub(u"[\u2003 ]", ",", mloc.group(1).strip()).strip()
        mpos = re.search(u"职能：(.+?)\s*(行业|$)", line)
        if mpos:
            expectinfo["expect_position_name"] = re.sub(u"[\u2003 ]", ",", mpos.group(1).strip()).strip()
        mindus = re.search(u"行业：(.+)$", line)
        if mindus:
            expectinfo["expect_industry_name"] = re.sub(u"[\u2003 ]", ",", mindus.group(1).strip()).strip()
        msalary = re.search(u"^期望薪资：(.+)$", line)
        if msalary:
            expectsalary = msalary.group(1).strip()
            m_monthsal = re.search("(?P<f>\d{3,5})-(?P<t>\d{3,5})", expectsalary)
            if m_monthsal:
                expectinfo["expect_salary_from"] = float(m_monthsal.group('f'))/1000.0
                expectinfo["expect_salary_to"] = float(m_monthsal.group('t'))/1000.0

        if selfremark:
            expectinfo["self_remark"] += "\n"+line
        mselfremark = re.search(u"^自我评价：(.+)", line)
        if mselfremark:
            expectinfo["self_remark"] = re.sub(u"自我评价：","",line).strip()
            selfremark = True
    return expectinfo


def extract_workinfo(text):
    work = resume_struct.get_emplyment_struct()
    work["ori_text"] = text
    last_industry = False

    for line in text.split('\n'):
        m_company = re.search(work_reg, line)
        if m_company:
            timestamp = match_timestamp.match_timestamp_by_reg(work_reg, line)
            work["corporation_name"] = m_company.group("company").strip()
            work["corporation_name"] = clean_company_name(work["corporation_name"])
            work["start_time"], work["end_time"], work["so_far"] = StringUtils.transform_timestamp(timestamp)
        m_position = re.search(u"职位名称(：|:)(?P<pos>.+)部门(：|:)(?P<arc>.+)", line)
        if m_position:
            work["position_name"] = m_position.group("pos").replace(u"(兼职)", "").strip()
            work["architecture_name"] = m_position.group("arc")
        m_industry = re.search(u"(行业|所属行业)(：|:)(?P<ind>.+?)(\s|$)", line)
        if m_industry:
            work["industry_name"] = m_industry.group("ind").strip()
            last_industry = True
            continue
        if not work["position_name"] and last_industry and len(line.split("\t")) == 2:
            work["position_name"] = line.split("\t")[1].strip()
            continue
        if last_industry:
            work["responsibilities"] += "\n"+line if work["responsibilities"] else line
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

    lastline = "not found project"
    isResp, isDesc = False,False
    for line in text.split('\n'):
        if lastline == "not found project":
            m_proj = re.search(project_reg, line)
            if m_proj:
                timestamp = match_timestamp.match_timestamp_by_reg(project_reg, line)
                project["name"] = m_proj.group("project").strip()
                project["name"] = re.sub(u"已关联$", "", project["name"]).strip()
                project["start_time"], project["end_time"], project["so_far"] = StringUtils.transform_timestamp(timestamp)
                lastline = "project"
            pass
        elif lastline == "project":
            m_desc = re.search(u"项目描述(:|：)", line)
            if m_desc:
                line = re.sub(u"项目描述(:|：)","", line).strip()
                isDesc, isResp = True, False
            m_resp = re.search(u"责任描述(:|：)", line)
            if m_resp:
                line = re.sub(u"责任描述(:|：)","", line).strip()
                isDesc, isResp = False, True
            pass
            if isDesc: project["describe"] += '\n'+line if project["describe"] else line
            if isResp: project["responsibilities"] += '\n'+line if project["responsibilities"] else line
    pass
    return project

def extract_languageinfo(text):
    lang = resume_struct.get_language_struct()

    for line in text.split('\n'):
        language = match_basic.match_language(re.split("\s+", line)[0])
        if language:
            lang["name"] = language.strip()
            lang["level"] = re.split("\s+", line)[1].strip()
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

    for line in text.split('\n'):
        m_train = re.search(train_reg, line)
        if m_train:
            timestamp = match_timestamp.match_timestamp_by_reg(train_reg, line)
            train["start_time"], train["end_time"], train["so_far"] = StringUtils.transform_timestamp(timestamp)
            train["name"] = m_train.group("train").strip()
            if len(train["name"].split("\t"))==2:
                train["authority"] = train["name"].split("\t")[0]
                train["name"] = train["name"].split("\t")[1]

        mauth = re.search(u"^培训机构：(.+)", line)
        if mauth:
            train["authority"] = mauth.group(1).strip()
        mcity = re.search(u"^培训地点：(.+)", line)
        if mcity:
            train["city"] = mcity.group(1).strip()
        mdesc = re.search(u"^培训描述：(.+)", line)
        if mdesc:
            train["description"] = mdesc.group(1).strip()

    return train

def extract_skillinfo(text):
    skill = resume_struct.get_skill_struct()

    for line in text.split('\n'):
        m_skill = re.search(skill_reg, line)
        if m_skill:
            skill["name"] = m_skill.group(1).strip()
            skill["level"] = m_skill.group(2).strip()

    return skill



###### 51job_0 template config
# 51job headlines
Headline_Dict={}
Headline_Dict[u"个人信息"] =  0
Headline_Dict[u"求职意向"] =  2
Headline_Dict[u"教育经历"] =  5
Headline_Dict[u"工作经验"] =  4
Headline_Dict[u"工作经历"] =  4
Headline_Dict[u"项目经验"] =  6
Headline_Dict[u"语言能力"] =  8
Headline_Dict[u"语言"] =  8
Headline_Dict[u"技能"]   = 10
Headline_Dict[u"IT技能"]   = 10

Headline_Dict[u"所获奖项"] = 99
Headline_Dict[u"培训经历"] =  9
Headline_Dict[u"在校情况"] = 99
Headline_Dict[u"最近工作"] = 99
Headline_Dict[u"自我评价"] = 99
Headline_Dict[u"技能特长"] = 99
Headline_Dict[u"社会经验"] = 99
Headline_Dict[u"校内职务"] = 99
Headline_Dict[u"其他信息"] = 99
Headline_Dict[u"证书"]     =  7
Headline_Dict[u"附件"]     = 99

# 51job edu config
edu_reg = u"(?P<sy>\d{4})\s*/\s*(?P<sm>\d{1,2})-{1,2}(((?P<ey>\d{4})\s*/\s*(?P<em>\d{1,2}))|(?P<ep>至今))\s*\t+(?P<school>.+?)\t+(?P<disc>.+?)\t+(?P<degree>.+)"

# 51job work config
work_reg = u"^(?P<sy>\d{4})\s*/(?P<sm>\d{1,2})\s*-{1,2}\s*((?P<ey>\d{4})\s*/(?P<em>\d{1,2})|(?P<ep>至今))\s*(?P<company>.+\s).+(\[\s*\d+\s*年|\s*\d+\s*个月)"

# 51job project config
project_reg = u"^(?P<sy>\d{4})\s*/(?P<sm>\d{1,2})-{1,2}((?P<ey>\d{4})\s*/(?P<em>\d{1,2})|(?P<ep>至今))(?P<project>.+)"

certi_reg = u"^(?P<sy>\d{4})\s*/(?P<sm>\d{1,2})\s+(?P<name>.+)"

train_reg = u"^(?P<sy>\d{4})\s*/(?P<sm>\d{1,2})-{1,2}((?P<ey>\d{4})\s*/(?P<em>\d{1,2})|(?P<ep>至今))\s*(：|:)\s*\t(?P<train>.+)"

skill_reg = u"(.+?)\t+(.+?)\t(.+)"
