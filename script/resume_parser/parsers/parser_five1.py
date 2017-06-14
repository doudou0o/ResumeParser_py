#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
import logging

import parser_basic
import templates
from resume_parser import divideModule

logger = logging.getLogger("mylog")
"""
51job parser
the origin 51job parser

"""

pname = "five1_parse"

def _parse_basic_info(extract_basicinfo, text):
    """
    itype: extract_basicinfo: function
    itype: text unicode
    rtype: basic struct
    """
    return extract_basicinfo(text)

def _parse_contact_info(extract_contactinfo, text):
    """
    itype: extract_contactinfo: function
    itype: text unicode
    rtype: contact struct
    """
    return extract_contactinfo(text)

def _parse_education_info(split_eduexp_block, extract_eduinfo, text):
    """
    itype: split_eduexp_block: function
    itype: extract_eduinfo: function
    itype: text unicode
    rtype: edu struct
    """
    edu_info_list = []
    exp_blocks = split_eduexp_block(text)
    for exp in exp_blocks:
        edu_info = extract_eduinfo(exp)
        if "school_name" not in edu_info or not edu_info["school_name"]:
            continue
        # judge
        # TODO
        edu_info_list.append(edu_info)
    pass
    return edu_info_list

def _parse_employment_info(split_workexp_block, extract_workinfo, text):
    """
    itype: split_workexp_block: function
    itype: extract_workinfo: function
    itype: text unicode
    rtype: work struct
    """
    work_info_list = []
    exp_blocks = split_workexp_block(text)
    for exp in exp_blocks:
        work_info = extract_workinfo(exp)
        if "corporation_name" not in work_info or not work_info["corporation_name"]:
            continue
        # judge
        # TODO
        work_info_list.append(work_info)
    pass
    return work_info_list

def _parse_project_info(split_project_block, extract_projectinfo, text):
    """
    itype: split_project_block: function
    itype: extract_projectinfo: function
    itype: text unicode
    rtype: project struct
    """
    project_info_list = []
    exp_blocks = split_project_block(text)
    for exp in exp_blocks:
        proj_info = extract_projectinfo(exp)
        if "name" not in proj_info or not proj_info["name"]:
            continue
        # judge
        # TODO
        project_info_list.append(proj_info)
    pass
    return project_info_list


def _parse_expect_info(extract_expectinfo, text):
    """
    itype: extract_expectinfo: function
    itype: text unicode
    rtype: map
    """
    return extract_expectinfo(text)

def _parse_language_info(split_language_block, extract_languageinfo, text):
    """
    itype: split_lang_block: function
    itype: extract_langinfo: function
    itype: text unicode
    rtype: language struct
    """
    language_info_list = []
    exp_blocks = split_language_block(text)
    for exp in exp_blocks:
        language_info = extract_languageinfo(exp)
        if "name" not in language_info or not language_info["name"]:
            continue
        language_info_list.append(language_info)
    pass
    return language_info_list

def _parse_certificate_info(split_certificate_block, extract_certinfo, text):
    """
    itype: split_certificate_block: function
    itype: extract_certinfo: function
    itype: text unicode
    rtype: train struct
    """
    train_info_list = []
    exp_blocks = split_certificate_block(text)
    for exp in exp_blocks:
        train_info = extract_certinfo(exp)
        if "name" not in train_info or not train_info["name"]:
            continue
        train_info_list.append(train_info)
    pass
    return train_info_list

def _parse_train_info(split_train_block, extract_traininfo, text):
    """
    itype: split_train_block: function
    itype: extract_traininfo: function
    itype: text unicode
    rtype: train struct
    """
    certi_info_list = []
    exp_blocks = split_train_block(text)
    for exp in exp_blocks:
        certi_info = extract_traininfo(exp)
        # judge
        # TODO
        certi_info_list.append(certi_info)
    pass
    return certi_info_list

def _get_parse_func_dict(template):
    """
    可配置方式: 一个配置方法
    如果出现需要模块整体需要修正的模板出现可以重写之
    其他方法可以复用
    """
    _parseinfo_func_dict = {}
    ## basic
    _parseinfo_func_dict[0]  = partial(_parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[3]  = partial(_parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[99] = partial(_parse_basic_info, template.extract_basicinfo)
    ## expect
    _parseinfo_func_dict[2]  = partial(_parse_expect_info, template.extract_expectinfo)
    ## contact
    _parseinfo_func_dict[1] = partial(_parse_contact_info, template.extract_contactinfo)
    ## employment
    _parseinfo_func_dict[4] = partial(_parse_employment_info,
            template.split_workexp_block, template.extract_workinfo
            )
    ## education
    _parseinfo_func_dict[5] = partial(_parse_education_info,
            template.split_eduexp_block, template.extract_eduinfo
            )
    ## project
    _parseinfo_func_dict[6] = partial(_parse_project_info,
            template.split_project_block, template.extract_projectinfo
            )
    ## certificate
    _parseinfo_func_dict[7] = partial(_parse_certificate_info,
            template.split_certificate_block, template.extract_certinfo
            )
    ## language
    _parseinfo_func_dict[8] = partial(_parse_language_info,
            template.split_language_block, template.extract_languageinfo
            )
    ## train
    _parseinfo_func_dict[9] = partial(_parse_train_info,
            template.split_train_block, template.extract_traininfo
            )

    return _parseinfo_func_dict


def parse(filename, filetext, fileori):

    # TODO
    # filename can used to parse or confirm name in resume

    for template in templates.get_parse_templates(pname):
        logger.debug("parser:%s run a mission" % (pname+template.template_name))

        real_parser = partial(parser_basic.parse,
                        template.split_headline_block,
                        _get_parse_func_dict(template),
                        pname+template.template_name)
        # go go go
        resume_ret = real_parser(filetext)

        if len(resume_ret["work"]) < 1 and \
                len(divideModule.getBlockByid(resume_ret["ori_block_text"], 4).split("\n"))>5:
            logger.info("parser:%s miss work" % (pname+template.template_name))
            continue

        if len(resume_ret["education"]) < 1 and \
                len(divideModule.getBlockByid(resume_ret["ori_block_text"], 5).split("\n"))>5:
            logger.info("parser:%s miss edu" % (pname+template.template_name))
            continue

        if len(resume_ret["work"]) < 1 and len(resume_ret["education"]) < 1:
            logger.info("parser:%s miss all work and edu" % (pname+template.template_name))
            continue

        # get contact from basic
        if "contact_phone" in resume_ret["basic"]:
            resume_ret["contact"]["phone"] = resume_ret["basic"]["contact_phone"]
        if "contact_tel" in resume_ret["basic"]:
            resume_ret["contact"]["tel"] = resume_ret["basic"]["contact_tel"]
        if "contact_email" in resume_ret["basic"]:
            resume_ret["contact"]["email"] = resume_ret["basic"]["contact_email"]

        # add resume name
        resume_ret["basic"]["resume_name"] = filename

        logger.info("parser:%s passed and return one result" % (pname+template.template_name))
        return resume_ret

    return None


def match(filetext):
    # TODO
    # 4 templary, this function is directly invoke parse()
    return parse is None



