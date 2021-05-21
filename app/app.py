#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/19 10:49
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : app.py
# @Desc    :
import os
import shutil
import tkinter
from datetime import datetime, timedelta
from tkinter import messagebox

import win32api
from loguru import logger

from app.versions import Versions
from config.baseconf import AppConf, VerConf


class App:
    def __init__(self):
        # 实例化窗口程序,并且隐藏窗口
        self._ui = tkinter.Tk()
        self._ui.withdraw()
        self._ver = Versions()

    def run(self):
        """
        1.判断当前目录下是否有versions文件夹,如果没有就报错
        2.遍历versions下的文件夹名字,组成版本号列表
        3.通过版本号类处理,得出最新的和倒数第二的版本号
        4.判断最新的版本号里面是否有配置文件,如果有直接启动程序
        5.如果没有就从倒数第二的开始复制配置文件到最新的版本文件夹内,启动程序
        :return:
        """
        if not os.path.exists(AppConf.VERSIONS_PATH):
            messagebox.showerror(title='错误', message='缺失启动文件')
            return
        verList = self._get_versions()
        self._ver.add_version_list(verList)

        # 启动EXE
        state = self._start_exe()
        if not state:
            return

        # 添加第二个版本号到配置文件中
        self._add_second_version()

        # 执行删除过期的文件夹
        self._remove()

        # 销毁窗口
        self._ui.destroy()

    def _remove(self):
        """
        删除过期的文件夹
        :return:
        """
        removeDict = VerConf.REMOVE_DICT
        removeKeyList = []
        for ver, removeTime in removeDict.items():
            if ver == self._ver.latestVer:
                continue
            if isinstance(removeTime, datetime):
                if (datetime.now() - removeTime).seconds <= 0:
                    continue
            verDir = os.path.abspath(os.path.join(AppConf.VERSIONS_PATH, ver))
            if os.path.exists(verDir):
                try:
                    # 文件夹存在,执行删除文件夹的操作,版本号信息在下次启动的时候回自动删除
                    shutil.rmtree(verDir)
                except:
                    logger.exception(f'删除文件夹失败:{verDir}')
            else:
                # 文件夹不存在,加入到removeKeyList中,遍历完成后集中删除
                removeKeyList.append(ver)

        # 删除对应的item
        for key in removeKeyList:
            if key in removeDict.keys():
                removeDict.pop(key)
        # 保存配置文件
        VerConf.set('REMOVE_DICT', removeDict)

    def _add_second_version(self):
        """
        添加第二个版本号到配置文件中
        :return:
        """
        secondVer = self._ver.secondVer
        if not VerConf.REMOVE_DICT:
            VerConf.REMOVE_DICT = {}
        removeDict = VerConf.REMOVE_DICT
        if not secondVer or secondVer in removeDict.keys():
            return
        removeTime = datetime.now() + timedelta(days=AppConf.REMOVE_INTERVAL)
        removeDict[secondVer] = removeTime
        VerConf.set('REMOVE_DICT', removeDict)

    def _start_exe(self) -> bool:
        """
        启动最新的exe文件
        :return: 启动成功返回真,否则返回假
        """
        latestVer = self._ver.latestVer
        latestConfPath = self._conf_path(latestVer)
        exePath = self._exe_path(latestVer)
        if not latestVer:
            messagebox.showerror(title='错误', message=f'缺失启动文件:{latestVer}')
            return False

        if not os.path.exists(exePath):
            messagebox.showerror(title='错误', message=f'缺失启动文件:{exePath}')
            return False

        # 复制配置文件
        self._copy_conf(latestConfPath)

        # 运行EXE文件,需要切换目录,不然会导致释放的文件会在启动器目录
        _tmpDir = os.getcwd()
        os.chdir(os.path.abspath(os.path.dirname(exePath)))
        win32api.ShellExecute(0, 'open', exePath, '', '', 1)
        os.chdir(_tmpDir)
        return True

    def _copy_conf(self, latestConfPath):
        """
        复制配置文件
        :param latestConfPath:最新版本配置文件路径
        :return:
        """
        if os.path.exists(latestConfPath):
            secondVer = self._ver.secondVer
            secondConfPath = self._conf_path(secondVer)
            if os.path.exists(secondConfPath):
                shutil.copy(secondConfPath, latestConfPath)
                logger.info(f'复制配置文件:{secondConfPath} 到 {latestConfPath}')

    @staticmethod
    def _conf_path(version: str):
        """
        根据版本号获取对应的配置文件路径
        :param version:
        :return:
        """
        return os.path.join(AppConf.VERSIONS_PATH, version, AppConf.CONF_FILE_NAME)

    @staticmethod
    def _exe_path(version: str):
        """
        根据版本号获取对应的启动文件路径
        :param version:
        :return:
        """
        return os.path.abspath(os.path.join(AppConf.VERSIONS_PATH, version, AppConf.TARGET_EXE))

    @staticmethod
    def _get_versions() -> list:
        verList = []
        fileList = os.listdir(AppConf.VERSIONS_PATH)
        for file in fileList:
            if os.path.isdir(os.path.join(AppConf.VERSIONS_PATH, file)):
                verList.append(file)
        return verList

    def _close_ui(self):
        self._ui.destroy()
