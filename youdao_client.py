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
    r = commands.getoutput(cmd)
    return r

def system(cmd, log=True):
    subprocess.Popen(cmd, shell=True)

def query(word):
    url = 'http://dict.youdao.com/search?le=eng&q=%s' % word    # 这个页面太烂了, 毫无优化可言. 还是用API把.
    data = urllib2.urlopen(url).read()
    #regex is slow
    begin = data.find('<div id="results-contents"')
    end = data.find('<!--例句选项卡 begin-->')
    return data[begin:end].replace(' ', '')

#chrome 插件用的是: http://dict.youdao.com/fsearch?pos=-1&doctype=xml&xmlVersion=3.2&dogVersion=1.0&vendor=unknown&appVer=3.1.17.4208&le=eng&q=hello
#xml格式.

def query(word):
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q=' + word
    data = urllib2.urlopen(url).read()
    print data
    return json_decode(data)

def pronounce(word):
    url = 'http://dict.youdao.com/dictvoice?audio=%s' % word
    data = urllib2.urlopen(url).read()
    f = tempfile.NamedTemporaryFile(delete=False)
    #print f.name
    f.write(data)
    f.flush()
    f.close()
    #print '------------ play!'
    cmd = 'nohup mplayer %s && rm %s 2>/dev/null ' % (f.name, f.name)
    system(cmd)
    #print '------------ done!'

def main():
    print query('hello')
    pronounce('hello')
    pass

if __name__ == "__main__":
    main()
