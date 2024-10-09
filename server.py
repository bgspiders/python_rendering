#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：python_rendering 
@File    ：server.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：9/10/2024 上午9:43 
'''
from sanic import Sanic
from sanic.exceptions import NotFound
app = Sanic("bgspider")
from sanic.response import json as jsonly
from util.func import *
from logger import logging
@app.get("/")
async def root(request):
    return jsonly({"message": "Hello World"})
@app.route('/', methods=['POST'])
async def handle_post(request):
    data = request.body
    fetch = json.loads(data)
    request_timeout = int(fetch.get('request_timeout',5))
    if request_timeout>REQUEST_TIMEOUT_MAX:
        request_timeout = REQUEST_TIMEOUT_MAX
    if 'http' not in fetch['url']:
        logging.debug(f"【为本地ip，禁止访问】{fetch['url']}")
        return jsonly({"content": "url异常"})
    if is_local_ip(fetch['url']):
        logging.debug(f"【准备渲染】{fetch['url']}")
        _len=await get_redis_lenth()
        if not _len :
            logging.debug('当前没有空闲端口,等待3秒后重试')
            return jsonly({"content": "当前没有空闲端口,等待3秒后重试"})
        task_num=put_redis(fetch)
        future=await get_content(task_num,request_timeout)
        return jsonly(future)
    else:
        logging.debug(f"【为本地ip，禁止访问】{fetch['url']}")
        return jsonly({"content": "地址异常，错误请求，请检查url"})

@app.exception(NotFound)
async def not_fount(request, exception):
    return jsonly({"message": "404"})

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,dev=False, debug=False, access_log=False)