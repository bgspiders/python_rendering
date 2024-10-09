#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：python_rendering 
@File    ：db.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：9/10/2024 上午9:48 
'''
import redis
from env import *
redis_server=redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB )
