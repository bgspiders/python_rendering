#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：python_rendering 
@File    ：env.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：9/10/2024 上午9:48 
'''
################redis配置############################
REDIS_HOST='127.0.0.1'
REDIS_PASSWORD=''
REDIS_PORT='6379'
REDIS_DB='1'
REDIS_TTL=300
REDIS_KEY='bg'
##############浏览器配置相关##########################
#打开浏览的个数
DP_NUM=2
#每个机器的线程数量
PAGE_THREAD=5
REQUEST_TIMEOUT_MAX=20
#打开完毕之后，睡眠时间
PAGE_TIMEOUT=0.3