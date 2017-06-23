#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resume_parser import divideModule
from resume_parser import resume_struct

"""
basic parser:
give a method to reuse parse process
it is not a real parser. it is a currying method.
it is used by other parsers which implemented such functions,
split_headlineblock_function, and parse function for each block.
"""

def basic_parse(split_headlineblock_func=None, parse_func_dict=None, pname="", text="" ):

    resume_ret = resume_struct.get_resume_struct(pname)

    blocks = split_headlineblock_func(text)

    # save ori block text
    resume_ret["ori_block_text"] = divideModule.text_HeadlineBlock(blocks)

    for titles, btext in blocks:
        for bid in titles:
            if bid not in parse_func_dict:continue

            # parse
            m_pret = parse_func_dict[bid](btext)

            if not m_pret:continue

            # update resume_ret
            if   type(resume_ret[_getNameByBid(bid)]) == dict:
                resume_ret[_getNameByBid(bid)].update(m_pret)
            elif type(resume_ret[_getNameByBid(bid)]) == list:
                resume_ret[_getNameByBid(bid)].extend(m_pret)
            else:
                resume_ret[_getNameByBid(bid)] = m_pret
        pass
    pass

    return resume_ret



def _getNameByBid(bid):
    return divideModule.getNameByBid(bid)

def parse_basic_info(extract_basicinfo, text):
    """
    itype: extract_basicinfo: function
    itype: text unicode
    rtype: basic struct
    """
    return extract_basicinfo(text)

def parse_contact_info(extract_contactinfo, text):
    """
    itype: extract_contactinfo: function
    itype: text unicode
    rtype: contact struct
    """
    return extract_contactinfo(text)

def parse_education_info(split_eduexp_block, extract_eduinfo, text):
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

def parse_employment_info(split_workexp_block, extract_workinfo, text):
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

def parse_project_info(split_project_block, extract_projectinfo, text):
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


def parse_expect_info(extract_expectinfo, text):
    """
    itype: extract_expectinfo: function
    itype: text unicode
    rtype: map
    """
    return extract_expectinfo(text)

def parse_language_info(split_language_block, extract_languageinfo, text):
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

def parse_train_info(split_train_block, extract_traininfo, text):
    """
    itype: split_train_block: function
    itype: extract_traininfo: function
    itype: text unicode
    rtype: train struct
    """
    train_info_list = []
    exp_blocks = split_train_block(text)
    for exp in exp_blocks:
        train_info = extract_traininfo(exp)
        if "name" not in train_info or not train_info["name"]:
            continue
        train_info_list.append(train_info)
    pass
    return train_info_list

def parse_certificate_info(split_certificate_block, extract_certinfo, text):
    """
    itype: split_certificate_block: function
    itype: extract_certinfo: function
    itype: text unicode
    rtype: train struct
    """
    certi_info_list = []
    exp_blocks = split_certificate_block(text)
    for exp in exp_blocks:
        certi_info = extract_certinfo(exp)
        # judge
        # TODO
        certi_info_list.append(certi_info)
    pass
    return certi_info_list

