#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 10:55
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : Launcher.py
# @Desc    :
from app import run_app
from config.baseconf import AppConf

# pyinstaller --clean --win-private-assemblies -F -w -i resource\GTR.ico Launcher.py
# pyinstaller -D Launcher.py

if __name__ == '__main__':
    AppConf.TARGET_EXE = 'GTR.exe'  # 目标文件名称
    run_app()
