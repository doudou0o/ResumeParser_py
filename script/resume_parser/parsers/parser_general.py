#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
import logging

import parser_basic
from resume_parser import divideModule
from templates import general_helper as helper

logger = logging.getLogger("mylog")
"""
general parser
"""

pname = "general_parse"

def _split_headline_block(filetext):
    """
    rtype: list[[titiles], text]
    """
    blocks = divideModule.divideHeadlineBlock(filetext)
    # TODO two resumes and next is eng
    # TODO merge two blocks with same title
    # TODO if projects in work, do merge
    return blocks

def _parse_basic_info(text):
    """
    itype: extract_basicinfo: function
    itype: text: unicode
    rtype: basic struct
    """
    pass

def _parse_education_info(text):
    """
    itype: split_eduexp_block: function
    itype: extract_eduinfo: function
    itype: text: unicode
    rtype: edu struct
    """
    edu_info_list = []

    line_tags, tag_text = helper.tag_eduinfo(text)

    line_tags, tag_text = helper.handle_edu_tags(line_tags, tag_text)

    exp_tags_blocks = helper.split_eduexp_block(line_tags, tag_text)

    for exp, tags in exp_tags_blocks:
        edu_info = helper.extract_eduinfo(tags, exp)
        if "school_name" not in edu_info or not edu_info["school_name"]:
            continue
        # judge
        # TODO
        edu_info_list.append(edu_info)
    pass
    return edu_info_list


def _get_parse_func_dict():
    """
    """
    _parseinfo_func_dict = {}
    ## basic
    ## expect
    ## contact
    ## employment
    ## education
    ## project
    ## certificate
    return _parseinfo_func_dict

def parse(filename, filetext, fileori):
    logger.debug("general parse run a mission")
    logger.info("general parse tempary closed")
    return None

    parse = partial(parser_basic.parse,
                        _split_headline_block,
                        _get_parse_func_dict(),
                        pname)

    # go go go
    resume_ret = parse(filetext)

    # judge
    # add resume name
    resume_ret["basic"]["resume_name"] = filename

    return resume_ret

