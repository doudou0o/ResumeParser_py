#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
import logging

from parser_basic import *
import templates
from resume_parser import divideModule

logger = logging.getLogger("mylog")
"""
zhilian parser
the origin zhilian parser

"""

pname = "zhilian_parse"

def _get_parse_func_dict(template):
    """
    可配置方式: 一个配置方法
    如果出现需要模块整体需要修正的模板出现可以重写之
    其他方法可以复用
    """
    _parseinfo_func_dict = {}
    ## basic
    _parseinfo_func_dict[0]  = partial(parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[3]  = partial(parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[99] = partial(parse_basic_info, template.extract_basicinfo)
    ## expect
    _parseinfo_func_dict[2]  = partial(parse_expect_info, template.extract_expectinfo)
    ## contact
    _parseinfo_func_dict[1] = partial(parse_contact_info, template.extract_contactinfo)
    ## employment
    _parseinfo_func_dict[4] = partial(parse_employment_info,
            template.split_workexp_block, template.extract_workinfo
            )
    ## education
    _parseinfo_func_dict[5] = partial(parse_education_info,
            template.split_eduexp_block, template.extract_eduinfo
            )
    ## project
    _parseinfo_func_dict[6] = partial(parse_project_info,
            template.split_project_block, template.extract_projectinfo
            )
    ## certificate
    _parseinfo_func_dict[7] = partial(parse_certificate_info,
            template.split_certificate_block, template.extract_certinfo
            )
    ## language
    _parseinfo_func_dict[8] = partial(parse_language_info,
            template.split_language_block, template.extract_languageinfo
            )
    ## train
    _parseinfo_func_dict[9] = partial(parse_train_info,
            template.split_train_block, template.extract_traininfo
            )

    ## skill
    _parseinfo_func_dict[10] = partial(parse_skill_info,
            template.split_skill_block, template.extract_skillinfo
            )

    return _parseinfo_func_dict


def parse(filename, filetext, fileori):
    # TODO
    # filename can used to parse or confirm name in resume

    for template in templates.get_parse_templates(pname):
        logger.debug("parser:%s run a mission" % (pname+template.template_name))

        real_parser = partial(basic_parse,
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

