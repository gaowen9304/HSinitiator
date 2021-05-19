#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 8:43
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : __init__.py.py
# @Desc    :
from app.app import App
from config.const import Const
from libs.log import init_log


def run_app():
    init_log(logName=Const.APP_NAME)
    app = App()
    app.run()
