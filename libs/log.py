#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 15:30
# @Author  : 高文强
# @Email   : 1061183361@qq.com
# @File    : log.py
# @Desc    :

from loguru import logger


# @logger.catch
# @logger.catch(onerror=lambda _: sys.exit(1))
# logger.exception()


def init_log(logPath="", logName='log', console=True, retention="10 days", level='INFO', encoding='utf-8', enqueue=True,
             serialize=False):
    """
    初始化日志信息
    :param logPath:日志文件路径,完整路径,如r'C:\log.log'
    :param logName:日志文件名称,在logPath不存在的情况下起作用
    :param console:是否在控制台输出,默认为真
    :param retention: 默认保留配置文件时间为10天
    :param level: 默认记录的等级为 INFO (TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL)
    :param encoding: 编码默认为utf-8
    :param enqueue: 异步写入,默认为真
    :param serialize: 序列化为json,默认为假
    :return:
    """

    if not logPath:
        logPath = f"./logs/{logName}.log"
    if not console:
        logger.remove(handler_id=None)

    errPath = f'{logPath[:-4]}_ERR.log'  # 错误日志路径

    logger.add(logPath, level=level, enqueue=enqueue, serialize=serialize, encoding=encoding, retention=retention)
    logger.add(errPath, level="ERROR", enqueue=enqueue, serialize=serialize, encoding=encoding, retention=retention)
