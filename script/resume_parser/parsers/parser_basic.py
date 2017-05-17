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

def parse(split_headlineblock_func=None, parse_func_dict=None, pname="", text="" ):

    resume_ret = resume_struct.get_resume_struct(pname)

    blocks = split_headlineblock_func(text)
    divideModule.print_HeadlineBlock(blocks)

    for titles, btext in blocks:
        for bid in titles:
            if bid not in parse_func_dict:continue

            # parse
            m_pret = parse_func_dict[bid](btext)

            if not m_pret:continue

            # update resume_ret
            if   type(resume_ret[getNameByBid(bid)]) == dict:
                resume_ret[getNameByBid(bid)].update(m_pret)
            elif type(resume_ret[getNameByBid(bid)]) == list:
                resume_ret[getNameByBid(bid)].extend(m_pret)
            else:
                resume_ret[getNameByBid(bid)] = m_pret
        pass
    pass

    return resume_ret



def getNameByBid(bid):
    return divideModule.getNameByBid(bid)

