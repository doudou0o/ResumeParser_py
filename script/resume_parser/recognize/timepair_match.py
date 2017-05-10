#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def match_timestamp(text):
    # TODO
    pass


def match_timestamp_by_reg(text, reg):
    t_reg = re.compile(reg)
    m = t_reg.search(text)
    if m:
        pass
    else:
        return None




