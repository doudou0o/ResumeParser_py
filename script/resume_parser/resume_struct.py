#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

def get_resume_struct(parser_name):
    resume = copy.deepcopy(resume_struct)
    resume["parser_name"] = parser_name
    return resume

def get_basic_struct():
    return resume_basic_struct.copy()

def get_education_struct():
    return resume_edu_struct.copy()

def get_emplyment_struct():
    return resume_work_struct.copy()

def get_project_struct():
    return resume_project_struct.copy()

def get_language_struct():
    return resume_language_struct.copy()

def get_certificate_struct():
    return resume_cert_struct.copy()

def get_training_struct():
    return resume_train_struct.copy()

def getStructByKey(kname):
    if   kname == "education":
        return get_education_struct()
    elif kname == "work":
        return get_emplyment_struct()
    elif kname == "project":
        return get_project_struct()
    elif kname == "language":
        return get_language_struct()
    elif kname == "certificate":
        return get_certificate_struct()
    elif kname == "training":
        return get_training_struct()
    else:
        raise Exception("no such key name:" + str(kname))

def clean_result(ret):
    resume = get_resume_struct("")
    for key in resume:
        if   type(resume[key]) == dict:
            resume[key] = filter_json(ret[key], resume[key])
        elif type(resume[key]) == list:
            for v in ret[key]:
                resume[key].append(filter_json(v, getStructByKey(key)))
        else: resume[key] = ret.get(key, "")
    return resume

def filter_json(src, dst):
    for k in dst:
        dst[k] = src.get(k,"")
    return dst


# origin resume struct
resume_struct = {
        "source":{
            "src"           : "",
            "src_no"        : [],
            },
        "contact":{
            "phone"     : "",
            "phone_area": 1 ,
            "email"     : "",
            "qq"        : "",
            "tel"       : "",
            "sina"      : "",
            "ten"       : "",
            "msn"       : "",
            "wechat"    : "",
            },
        "basic":{
            "updated_at"  : "0000-00-00 00:00:00",
            "resume_name" : "",
            "is_validate" : "U",
            "name"        : "",
            "gender"      : "U",
            "birth"       : "",
            "age"         : 0 ,
            "marital"     : "U",
            "degree"      : 99 ,
            "current_status" : "",
            "work_experience"       : 0 ,
            "address_province"      : "",
            "address"               : "",
            "account_province"      : "",
            "account"               : "",
            "card"                  : "",
            "expect_work_at"        : "",
            "expect_industry_name"  : "",
            "expect_position_name"  : "",
            "expect_city_ids"       : "",
            "expect_city_names"     : "",
            "expect_salary_from"    : "",
            "expect_salary_to"      : "",
            "expect_annual_salary_from"    : "",
            "expect_annual_salary_to"      : "",
            "expect_salary_month"   : "",
            "self_remark"           : "",
            "my_project"            : "",
            # 其他
            "is_fertility"          : "U",
            "is_house"              : "U",
            "live_family"           : "U",
            "interests"             : "",
            "focused_corporations"  : "",
            "focused_feelings"      : "",
            "overseas"              : "N",
            "political_status"      : "",
            "expect_type"           : "",
            "expect_bonus"          : "",
            "project_info"          : "",
            "other_info"            : "",
            "not_expect_corporation_name"   : "",
            "not_expect_corporation_ids"    : "",
            "not_expect_corporation_status" : 0 ,
            },
        "work":[],
        "education":[],
        "project":[],
        "language":[],
        "certificate":[],
        "training":[],
}

# origin resume basic info struct
resume_basic_struct = {
    "updated_at"  : "0000-00-00 00:00:00",
    "resume_name" : "",
    "name"        : "",
    "gender"      : "U",
    "birth"       : "",
    "age"         : 0 ,
    "marital"     : "U",
    "current_status" : "",
    "work_experience"       : 0 ,
    "address_province"      : "",
    "address"               : "",
    "account_province"      : "",
    "account"               : "",
    "card"                  : "",
    "expect_work_at"        : "",
    "expect_industry_name"  : "",
    "expect_position_name"  : "",
    "expect_city_ids"       : "",
    "expect_city_names"     : "",
    "expect_salary_from"    : "",
    "expect_salary_to"      : "",
    "expect_salary_month"   : "",
    "expect_annual_salary_from"    : "",
    "expect_annual_salary_to"      : "",
    "basic_salary_from"    : "",
    "basic_salary_to"      : "",
    "basic_salary_month"   : "",
    "self_remark"          : "",
    # 其他
    "my_project"            : "",
    "degree"      : 99 ,
    "is_fertility"          : "U",
    "is_house"              : "U",
    "live_family"           : "U",
    "interests"             : "",
    "focused_corporations"  : "",
    "focused_feelings"      : "",
    "overseas"              : "N",
    "political_status"      : "",
    "expect_type"           : "",
    "expect_bonus"          : "",
    "project_info"          : "",
    "other_info"            : "",
    "not_expect_corporation_name"   : "",
    "not_expect_corporation_ids"    : "",
    "not_expect_corporation_status" : 0 ,
}

# origin resume work info struct
resume_work_struct = {
    "corporation_name"  : "",
    "start_time"        : "",
    "end_time"          : "",
    "so_far"            : "N",
    "corporation_desc"  : "",
    "corporation_type"  : "",
    "position_name"     : "",
    "responsibilities"  : "",
    "architecture_name" : "",
    "scale"             : "",
    "industry_name"     : "",
    "reporting_to"      : "",
    "subordinates_count": 0,
    "basic_salary_from" : "",
    "basic_salary_to"   : "",
    "salary_month"      : "",
    "annual_salary_from": "",
    "annual_salary_to"  : "",
    "management_experience" : "N",
     #其他
    "station_name"      : "",
    "bonus"             : "",
    "city"              : "",
}

# origin resume edu info struct
resume_edu_struct = {
    "school_name"       : "",
    "start_time"        : "",
    "end_time"          : "",
    "so_far"            : "N",
    "discipline_name"   : "",
    "degree"            : 99,
     # 其他
    "discipline_desc"   : "",
    "is_entrance"       : "Y",
}


# origin resume project info struct
resume_project_struct = {
    "name"              : "",
    "start_time"        : "",
    "end_time"          : "",
    "so_far"            : "N",
    "describe"          : "",
    "responsibilities"  : "",
    "achivement"        : "",
    "corporation_name"  : "",
    "position_name"     : "",
     # 其他
    "soft_env"          : "",
    "hard_env"          : "",
    "develop_tool"      : "",
}

# origin resume language info struct
resume_language_struct = {
    "name"            : "",
    "level"           : "",
    "certificate"     : "",
}


# origin resume certificate info struct
resume_cert_struct = {
    "name"              : "",
    "start_time"        : "",
    "description"       : "",
}

# origin resume training info struct
resume_train_struct = {
    "name"              : "",
    "start_time"        : "",
    "end_time"          : "",
    "so_far"            : "N",
    "city"              : "",
    "certificate"       : "",
    "authority"         : "",
    "description"       : "",
}

