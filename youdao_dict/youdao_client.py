#!/usr/bin/env python
#coding: utf-8
#author : ning
#date   : 2013-03-08 21:06:42

import urllib, urllib2
import os, sys
import re, time
import logging
import tempfile
import commands
import json
import subprocess

def json_encode(j):
    return json.dumps(j, indent=4)
def json_decode(j):
    return json.loads(j)

def system(cmd, log=True):
    subprocess.Popen(cmd, shell=True)

# query 有3个选择: 
# 1. 原始html页面:  /serarch?q=hello  好处是, 这个页面是有道的主页，性能上应该是最好的, 但是 这个页面太烂了, 毫无优化可言. 还是用API把.
# 2. open API: /openapi.do?q=hello    好处是json, 简单, 缺点是一般这种API服务器端都会有一些校验, 性能会较差.
# 3. chrome 插件用的API : /fsearch?q=hello  好处是性能, 格式好(xml), 但是方法2很简单, 姑且用2把.
def query(word):
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q=' + word
    data = urllib2.urlopen(url).read()
    #print data
    return json_decode(data)

#this is much simper, 3ks mplayer
def pronounce(word):
    url = 'http://dict.youdao.com/dictvoice?audio=%s' % word
    cmd = 'nohup mplayer "%s" >/dev/null 2>&1 ' % (url,)
    system(cmd)

def main():
    print query('hello')
    pronounce('hello')
    pass

if __name__ == "__main__":
    main()
