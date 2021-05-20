#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 16:58
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : conf.py
# @Desc    :
from config.baseconf import AppConf, VerConf


def init_conf():
    for conf in [AppConf, VerConf]:
        conf.load()

    if isinstance(VerConf.REMOVE_DICT, dict):
        VerConf.REMOVE_DICT = {}
