#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/4/22 15:12
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : baseconf.py
# @Desc    :
import abc
import os
from contextlib import contextmanager
from functools import reduce

import yaml
from loguru import logger

from config.const import Const
from libs.singleton import Singleton


class Conf(Singleton):
    confPath = None
    conf = None

    def save(self):
        """
        保存配置文件
        :return:
        """
        with open(self.confPath, "w", encoding="utf-8") as f:
            yaml.dump(self.conf, f, allow_unicode=True)

    def getValue(self, keyList, default=""):
        """
        根据路径获取值
        :param keyList: 要获取的值路径:['erp','name']
        :param default: 如果当前路径不存在,返回默认值
        :return:获取成功返回值内容,否则返回空
        """
        value = default
        try:
            if len(keyList) > 0:
                temp = None
                for i, k in enumerate(keyList):
                    if i == 0:
                        temp = self.conf
                    if not isinstance(temp, dict):
                        # print(f'当前信息不是字典类型:{temp}')
                        break
                    if k in temp.keys():
                        temp = temp[k]
                        continue
                    else:
                        # print(f'当前信息{temp=}不存在key={k}')
                        break
                else:
                    value = temp
        finally:
            return value

    def setValue(self, keyList, value):
        """
        根据提供的路径设置值
        :param keyList: 路径列表
        :param value: 要设置的值
        :return:设置成功返回真,否则返回假
        """
        if len(keyList) <= 0:
            return False
        result = True
        try:
            # 判断所有键值是否存在
            temp = None
            tempKList = []  # 已存在的key列表
            addKList = []  # 需要新增的key列表
            isDict = True
            for i, k in enumerate(keyList):
                if i == 0:
                    temp = self.conf
                if isinstance(temp, dict):
                    if k in temp.keys():
                        temp = temp[k]
                        tempKList.append(k)
                        continue
                    else:
                        addKList.append(k)
                        continue
                else:
                    if len(addKList) == 0:
                        isDict = False
                    addKList.append(k)

            if len(addKList) > 0:
                if not isDict:  # 需要把值先修改为字典信息
                    self._wirte_value(tempKList, {})
                fristKey = addKList.pop(0)
                tempKList.append(fristKey)
                value = reduce(lambda x, y: {y: x}, reversed(addKList), value)
            self._wirte_value(tempKList, value)

        except Exception as err:
            print(f'conf→setValue:{err}')
            result = False
        finally:
            return result

    def _wirte_value(self, keyList, value):
        """
        执行写入值操作
        :param keyList:key列表
        :param value: 要写入的值
        :return:
        """
        self.conf = self._update_value(self.conf, keyList, value)

    def _update_value(self, source, keyList, value):
        """
        更新字典信息
        :param source:原字典
        :param keyList:路径列表
        :param value:要修改的值
        :return:
        """
        if len(keyList) == 1:
            key = keyList[0]
            source[key] = value
            return source
        key = keyList.pop(0)
        retuned = self._update_value(source.get(key, {}), keyList, value)
        source[key] = retuned
        return source

    @contextmanager
    def auto_save(self):
        try:
            yield
            self.save()
            return True
        except Exception as e:
            logger.exception('配置信息保存失败')
            return False

    def remove_key(self, keyList):
        """
        删除键
        :param keyList: 键列表
        :return:
        """
        tmpDict = self.conf
        for key in keyList[:-1]:
            if key in tmpDict.keys():
                tmpDict = tmpDict[key]
                if not isinstance(tmpDict, dict):
                    # 不是字典,当前键列表不存在
                    break
            else:
                # 不是字典,当前键列表不存在
                break
        else:
            if keyList[-1] in tmpDict.keys():
                tmpDict.pop(keyList[-1])
                self.setValue(keyList[:-1], tmpDict)


def _build_conf(confPath: str = '', default: str = ''):
    """
    实例化conf对象
    :param confPath: 配置文件路径
    :param default: 默认配置信息
    :return:
    """
    # 判断文件是否存在,存在直接读取,不存在就读取字符串
    if os.path.exists(confPath):
        with open(confPath, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content:
            content = default
    else:
        # 文件不存在,默认文档信息
        content = default

    # 读取信息并转化为yaml对象
    _conf = yaml.load(content, yaml.FullLoader)

    Conf.conf = _conf
    Conf.confPath = confPath
    return Conf()


class BaseConf(abc.ABC):
    _confName = ''
    _fields = []
    _verify = {}
    _conf = _build_conf(Const.YMAL_PATH, Const.YMAL_DEFAULT)

    @classmethod
    def set(cls, key: str, value: any):
        result = False
        if not cls._fields:
            cls._fields = [v for v in dir(cls) if not callable(getattr(cls, v)) and v[0] != '_']

        if key and value is not None:
            with cls._conf.auto_save():
                result = cls._write_single(key, value)
        return result

    @classmethod
    def _write_single(cls, key, value):
        """
        设置单个内容
        :param key:
        :param value:
        :return: 写入成功返回真,否则返回假
        """
        if key not in cls._fields:
            return False
        if key in cls._verify.keys():
            allow, error, value = cls._verify[key](value)
            if not allow:
                logger.error(error)
                return False
        setattr(cls, key, value)
        cls._conf.setValue([cls._confName, key], value)
        return True

    @classmethod
    def load(cls):
        """
        加载配置文件
        :return:
        """
        if not cls._fields:
            cls._fields = [v for v in dir(cls) if not callable(getattr(cls, v)) and v[0] != '_']

        data = cls._conf.getValue([cls._confName])
        if not isinstance(data, dict):
            return
        for key, value in data.items():
            if key not in cls._fields:
                continue
            if key in cls._verify.keys():
                allow, error, value = cls._verify[key](value)
                if not allow:
                    logger.error(f'配置项加载失败:{key=} {value=} {error=}')
                    continue
            setattr(cls, key, value)


class AppConf(BaseConf):
    """app配置项"""
    _confName = "AppConf"  # 指定配置项的名称
    _verify = {}

    TARGET_EXE = ""  # 要运行的EXE文件名称,在最新版本号文件夹下必须存在
    VERSIONS_PATH = "./versions"  # 版本号文件夹路径,默认为程序目录下面的versions文件夹
    CONF_FILE_NAME = "conf.yml"  # 要启动软件的配置文件名
    REMOVE_INTERVAL = 3  # 默认删除旧版本的时间间隔为7天


class VerConf(BaseConf):
    """版本配置项"""
    _confName = "VerConf"  # 指定配置项的名称
    _verify = {}

    REMOVE_DICT = {}  # 删除版本文件夹的字典 {verName:delTime}
