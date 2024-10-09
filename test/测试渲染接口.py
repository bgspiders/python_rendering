#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：python_rendering 
@File    ：测试渲染接口.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：9/10/2024 上午9:53 
'''
import requests

url = 'http://127.0.0.1:8000'
data = {'url': "https://tools.bgspider.com",'request_timeout':20}
resp=requests.post(url=url,json=data)
print(resp.text)
