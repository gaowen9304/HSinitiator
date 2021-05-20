#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/4/22 16:45
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : singleton.py
# @Desc    : 单例模式
import threading


class Singleton:
    """单例模式,请注意,此单例实例化时会调用__init__方法"""
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return Singleton._instance
