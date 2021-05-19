#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 10:49
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : app.py
# @Desc    :
import tkinter
import tkinter.messagebox as mesaagebox


class App:
    def __init__(self):
        # 实例化窗口程序,并且隐藏窗口
        self._ui = tkinter.Tk()
        self._ui.withdraw()

    def run(self):
        """
        1.判断当前目录下是否有versions文件夹,如果没有就报错
        2.遍历versions下的文件夹名字,组成版本号列表
        3.通过版本号类处理,得出最新的和倒数第二的版本号
        4.判断最新的版本号里面是否有配置文件,如果有直接启动程序
        5.如果没有就从倒数第二的开始复制配置文件到最新的版本文件夹内,启动程序
        :return:
        """

        pass

    def _close_ui(self):
        self._ui.destroy()
