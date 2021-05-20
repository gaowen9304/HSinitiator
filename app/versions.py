#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 15:03
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : versions.py
# @Desc    :
import re


class Versions:
    """版本号要求只有数字和小数点"""

    def __init__(self):
        self._verList = []

    @property
    def latestVer(self):
        """
        最新的版本号
        :return:
        """
        _latestVer = self._verList[0] if self._verList else ''
        return _latestVer

    @property
    def secondVer(self):
        """
        倒数第二的版本号
        :return:
        """
        _secondVer = self._verList[1] if len(self._verList) >= 2 else ''
        return _secondVer

    def add_version_list(self, verList: list):
        verList = self._filter_vers(verList)
        self._verList = self._sort(verList)

    @staticmethod
    def _sort(verList: list):
        """
        对版本号列表进行排序
        :param verList:
        :return:
        """
        return sorted(verList, key=lambda x: tuple(int(v) for v in x.split(".")), reverse=True)

    def _filter_vers(self, verList: list) -> list:
        """
        过滤无意义的版本号元素
        :param verList:
        :return:
        """
        _tmpList = []
        for ver in verList:
            if self._is_chinese(ver) or not self._is_num_and_point(ver):
                continue
            _tmpList.append(ver)
        return _tmpList

    @staticmethod
    def _is_num_and_point(version: str) -> bool:
        """
        判断是否只包含了小数点和数字
        :param version: 版本号信息
        :return:
        """
        pattern = re.compile(r'^[.\d]*$')
        res = pattern.search(version)
        return bool(res)

    @staticmethod
    def _is_chinese(value):
        """
        检查整个字符串是否包含中文
        :param value: 需要检查的字符串
        :return: bool
        """
        for ch in value:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


if __name__ == '__main__':
    ver = Versions()
    print(f'{ver.latestVer=}')
    print(f'{ver.secondVer=}')
