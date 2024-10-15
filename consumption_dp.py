#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：remote_suite 
@File    ：consumption_dp.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：8/7/2024 上午10:03 
'''
# coding=utf-8
# -*- encoding: utf-8 -*-
import time
import traceback
import json
import  datetime
from DrissionPage._units.waiter import ElementWaiter
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._functions.by import By
import re, os
from util.db import *
import platform
GLOBAL_FILE_TOKEN=''
server_name = platform.node()
TAB_COUNT_NUM=0
OPEN_NUM_NO_PROXY=0
OPEN_NUM_IS_PROXY=0
OPEN_NUM_MAX=50
project_root = os.path.dirname(os.path.dirname(__file__))
GLOBAL_CONFIG={
}
from logger import logging
ip_list={
}
for _ in range(DP_NUM):
    ip_list[f'ip{_}']={'port': 10111+_, 'usr_path':f"tmp{_}", 'used_time': 0}
start_page=False
def close_other_tab(page):
    if page.tabs_count>1:
        for tab in page.tab_ids:
            page.close_tabs(tab)
    else:
        for tab in page.tab_ids:
            not_close_tab_list.append(tab)
        return False
no_proxy_list=list(ip_list.keys())
proxy_index=0
def poll(proxy=False):
    '''
    简单轮询
    '''
    global proxy_index
    p=no_proxy_list[proxy_index]
    proxy_index=(proxy_index+1)%len(no_proxy_list)
    return p
close_tab_list=['']
not_close_tab_list=[]
page_is_proxy,page_no_proxy=None,None
def init_page():
    global page_is_proxy,page_no_proxy,start_page,not_close_tab_list
    while True:
        try:
            if not start_page:
                for ip in ip_list.keys():
                    _config=ip_list[ip]
                    co = ChromiumOptions()
                    co.add_extension('extension')
                    co.no_imgs(True)
                    _ip=poll()
                    co.set_user_data_path(f'{ip_list[_ip]["usr_path"]}')
                    co.set_address(f'127.0.0.1:{ip_list[_ip]["port"]}')
                    GLOBAL_CONFIG[ip] = ChromiumPage(co)
                    close_other_tab(GLOBAL_CONFIG[ip])
                start_page = True
                logging.success('浏览器启动成功')
            else:
                close_timeout_page()
        except Exception as e:
            if '与页面的连接已断开' in str(e):
                start_page=False
        time.sleep(1)
def close_timeout_page():
    global page_used,page_no_proxy,page_is_proxy,start_page
    copy_dict=dict(page_used)
    try:
        if copy_dict:
            for k, v in copy_dict.items():
                if (int(time.time()) - int(v['time'])) > 120:
                    print(k)
                    page = GLOBAL_CONFIG[v['ip']]
                    page.close_tabs(k)
                    del page_used[k]
        else:
            for k, v in copy_dict.items():
                page=GLOBAL_CONFIG[k]
                for tab in page.tabs:
                    if page.tabs_count > 1:
                        if tab not in page_used.keys():
                            if tab not in not_close_tab_list:
                                if tab not in copy_dict.keys():
                                    port_use = {}
                                    port_use['time'] = time.time()
                                    port_use['tab'] = tab
                                    port_use['ip'] =k
                                    page_used[tab] = port_use
    except Exception as e:
        print(f'检测tab错误----{e}')
        start_page=False

page_used={}
def handle_request(fetch):
    global TAB_COUNT_NUM,OPEN_NUM_IS_PROXY,OPEN_NUM_NO_PROXY,page_no_proxy,page_is_proxy,start_page
    request_timeout = int(fetch['request_timeout'])
    if request_timeout>REQUEST_TIMEOUT_MAX:
        request_timeout = REQUEST_TIMEOUT_MAX
    page_timeout = int(fetch.get('page_timeout',PAGE_TIMEOUT))
    fetch_url = fetch['url']
    try:
        port_use={}
        _ip=poll(False)
        page=GLOBAL_CONFIG[poll(False)]
        port_use['ip'] = _ip
        page.set.cookies.clear()
        try:
            logging.debug(f'当前标签页的个数为{page.tabs_count}')
        except Exception as e:
            if '与页面的连接已断开' in str(e):
                start_page = False
            time.sleep(3)
        result={}
        tab_id=page.new_tab().tab_id
        port_use['time'] = time.time()
        port_use['tab'] = str(tab_id)
        page_used[str(tab_id)]=port_use
        close_timeout_page()
        _tab = page.get_tab(tab_id)
        _tab.get(url=fetch_url, retry=3, interval=1, timeout=request_timeout)
        # page.set.window.mini()
        time.sleep(page_timeout)
        _tab.stop_loading()
        result['url'] = _tab.url
        result['content'] = _tab.html
        result['cookies'] = _tab.cookies().as_dict()
    except Exception as e:
        logging.error(e)
        if '与页面的连接已断开' in str(e):
            start_page=False
        err_info = f"【渲染失败】{server_name}{_tab.url}" + str(traceback.format_exc()).replace("\r", "").replace("\n", "")
        logging.error(err_info)
        result['error'] = err_info
        result['status_code'] = 502
    finally:
        try:
            page.close_tabs(tab_id)
            logging.debug('tab已经关闭')
            copy_dict=dict(page_used)
            for k,v in copy_dict.items():
                if str(tab_id) ==v['tab']:
                    del page_used[str(tab_id)]
        except Exception as e :
            if '由于目标计算机积极拒绝，无法连接' in str(e):
                logging.error('标签页关闭判断错误')
            else:
                logging.error(f'关闭tab失败{e}')
        return result
import threading
connection_pool_redis = threading.local()
connection_pools = threading.local()
def get_connection_redis():
    # 每个线程的第一次调用该函数时，创建一个数据库连接
    if not hasattr(connection_pools, 'connection'):
        connection_pools.connection = redis_server
    return connection_pools.connection
start_count=[]
def run():
    connection_redis = get_connection_redis()
    while True:
        if start_page:
            _len = connection_redis.llen('keys')
            if _len>0:
                try:
                    key = connection_redis.blpop("keys", 1)
                    if key:
                        data=json.loads(key[1].decode())
                        feach=connection_redis.get(data)
                        if feach:
                            json_data=json.loads(feach.decode())
                            logging.debug(f"拿到任务{json_data['url']}")
                            save_data=handle_request(json_data)
                            connection_redis.setex(data+'_success', 300,json.dumps(save_data))
                        else:
                            logging.debug('此任务到期')
                except Exception as e:
                    time.sleep(0.3)
                    logging.error(e)
            else:
                time.sleep(0.3)
        else:
            time.sleep(5)
threads = []
thread = threading.Thread(target=init_page)
threads.append(thread)
thread.start()
for i in range(PAGE_THREAD):
    thread = threading.Thread(target=run)
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()