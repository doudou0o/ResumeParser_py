#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_resume_struct(parser_name):
    resume = resume_struct.copy()
    resume["parser_name"] = parser_name
    return resume

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
        "skill":[],
        "user_tag":[""],
        "setting":{
            "salary_is_visible"     : 1,
            },
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
