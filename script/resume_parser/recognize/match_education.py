#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resume_parser.utils import StringUtils

"""
this module is match item about education
such as: match_degree; match_school; match_discipline
"""

degree_dict={}
degree_list=[ 94,95, 6,4,3,2,1, 92,91,90,89,87,86, 99]

def match_degree(text, default=None):
    """
    itype: text unicode
    itype: default: if its confirmed degree, then default should be 99
    rtype: degree: int
    """
    text = _clean_text(text)
    for i in degree_list:
        for deg in degree_dict[i]:
            if -1 == text.find(deg):
                continue
            else:
                return i
    return default

def match_school(text):
    """
    itype: text unicode
    rtype: school_name
    """
    pass

def match_discipline(text):
    """
    itype: text unicode
    rtype: discipline_name
    """
    pass


def _clean_text(text):
    text = StringUtils.removeShapesSymbols(text)
    text = StringUtils.removeGeneralPunctuation(text)
    text = StringUtils.removeChSpace(text)
    text = text.lower()
    return text



degree_dict[1] = {u"本科", u"bachelor", }
degree_dict[2] = {u"硕士", u"研究生", u"master"}
degree_dict[3] = {u"博士", u"doctor"}
degree_dict[4] = {u"专科", u"大专", u"associate"}
degree_dict[6] = {u"mba"}

#degree_dict[10] = {u"博士后"}

degree_dict[86] = {u"初中", u"junior high"}
degree_dict[87] = {u"职高", u"skilled workers training"}
degree_dict[89] = {u"高中", u"senior high"}
degree_dict[90] = {u"中专"}
degree_dict[91] = {u"中技", u"技校"}
degree_dict[92] = {u"专升本"}
degree_dict[94] = {u"emba"}
degree_dict[95] = {u"mpa"}

degree_dict[99] = {u"其他", u"other"}


