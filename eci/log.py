# -*- coding: UTF-8 -*-

_debug = True
_now = 0
_sum = 0

def log_num(flag):
    if _debug :
        global _now,_sum
        _now += 1
        print "%s : %d / %d" %(flag,_now,_sum)

def reset(sum=0):
    global _now,_sum
    _now = 0
    _sum = sum