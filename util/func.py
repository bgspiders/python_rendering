#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：python_rendering 
@File    ：func.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：9/10/2024 上午9:47 
'''
import socket,re,time
from util.db import *
from uuid import uuid4
import asyncio
import json
def is_local_ip(ip_address):
    # 获取本机所有网络接口信息
    interfaces = socket.gethostbyname_ex(socket.gethostname())[2]
    interfaces_all=[re.findall('(\d+\.\d+)\.\d+.\d+',x)[0] for x in interfaces]+['127.0']
    ip=re.findall('(\d+\.\d+)\.\d+.\d+',ip_address)
    if ip:
        if ip[0] in interfaces_all:
            return False
        else:
            return True
    else:
        return True
def put_redis(data):
    task_number=str(uuid4())
    redis_server.setex(task_number,120,  json.dumps(data))
    redis_server.lpush('keys', json.dumps(task_number))
    return task_number
async def get_redis_lenth():
    lenth= redis_server.llen(REDIS_KEY)
    if lenth>20:
        return False
    else:
        return True
async def get_content(task_num,page_timeout):
    start_timeout=time.time()
    new_task_num=task_num+'_success'
    while True:
        if redis_server.exists(new_task_num):
            data=json.loads(redis_server.get(new_task_num).decode())
            print('渲染完毕，接口返回')
            return data
        else:
            await asyncio.sleep(0.3)
        stop_time=time.time()
        if (stop_time-start_timeout)>page_timeout:
            print(stop_time-start_timeout,page_timeout,'超时')
            return {}