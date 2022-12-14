#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   config.py
@Time    :   2022/08/18 20:29:13
@Author  :   Volker Lorrmann
@Version :   0.1
@Contact :   volker.lorrmann@gmail.com
@License :   (C)Copyright 2020-2022, Volker Lorrmann
@Desc    :   None
'''


from .utils import get_user_agents, get_webshare_proxy_list, get_free_proxy_list

USER_AGENTS = get_user_agents()

# Place your proxy list url from webshare.io here
URL_WEBSHARE_PROXY_LIST = None

if URL_WEBSHARE_PROXY_LIST is not None:
    PROXIES = get_webshare_proxy_list(URL_WEBSHARE_PROXY_LIST)
    
else:
    PROXIES = get_free_proxy_list()

# Add your list of proxies manually here
# PROXIES = ["http://my-own-proxy-1.abc:1234", "http://my-own-pwoxy-2.cdf:9876"]
