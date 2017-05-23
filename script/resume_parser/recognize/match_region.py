#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os



def remove_suffix_region(region):
    suffix = [ u"地区", u"自治州", u"自治县", u"省", u"市", u"县",u"区"]
    for suf in suffix:
        if region.endswith(suf):
            temp = region[:-1*len(suf)]
            if len(temp) >= 2:
                region = temp
            break
    return region


def region_relation_init():
    region_list = []
    region_relation = {}
    for line in open(os.path.join(os.path.dirname(__file__),"../resources/regions.txt")):
        line = line.strip().decode("utf8")
        items = line.split('\t')

        rid  = int(items[0])
        pid  = int(items[1])
        name = remove_suffix_region(items[2])
        lvl  = int(items[3])

        region_list.append([rid, name, lvl])

        if pid in region_relation:
            region_relation[pid].append([rid, name])
        else:
            region_relation[pid]=[ [rid, name], ]
    return region_list, region_relation


region_list,region_relation = region_relation_init()


def match_region(line):
    for rid, region, lvl in region_list:
        if region in line:
            if lvl <= 2:
                line = re.sub(region,"",line)
                childrens = region_relation[rid]
                for cid, child in childrens:
                    if child in line:
                        rid = cid
                        break
                return rid
            else:
                return rid
    return ""



if __name__ == '__main__':
    while(True):
        ans = raw_input("input:")
        ans = ans.decode("utf8")
        if ans == "end":
            break
        print match_region(ans)


