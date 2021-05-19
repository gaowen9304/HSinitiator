#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 16:58
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : conf.py
# @Desc    :


import os

import yaml

from config.const import Const


def init_conf():
    confPath = Const.CONF_PATH
    if not os.path.exists(confPath):
        raise AssertionError('配置文件不存在,请检查!')

    with open(confPath, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml.load(content, yaml.FullLoader)