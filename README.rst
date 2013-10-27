
用过的ubuntu下的字典
====================

:stardict: 
   StarDict hasn't seen any active development for many years
   推荐 GoldenDict
:GoldenDict: 
   确实不错, 但是占CPU. 常年占20%
:youdao:
    网页版而且有广告.
    chrome 插件不错. 

stardict, GoldenDict 的一个共同问题是, 查询结果的 **字体都是一样大小** . 很不好看.

youdao-dict-for-ubuntu 演示
===========================

http://v.youku.com/v_show/id_XNTI2ODQ1MjY4.html
http://v.youku.com/v_show/id_XNTI2ODYyMzUy.html

特点
====

1. 自动取词, 鼠标跟随
2. 发音.
3. 单词白名单
4. 用chrome 浏览器跳转到youdao查词.

5. 基于web版youdao , 而不是API(http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q=hello)
   因为API 通常有鉴权而比较慢.

.. image:: https://raw.github.com/idning/youdao-dict-for-ubuntu/master/imgs/youdao-dict.png
    :height: 355px


install
=======

0. 发声需要mplayer
1. pip install pygtk
2. TODO

开机启动
--------

在/etc/xdg/autostart下, 增加一个.desktop文件::

    root@ning-laptop:/etc/xdg/autostart# cat youdao-dict-for-ubuntu.desktop 
    [Desktop Entry]
    Name=youdao-dict-for-ubuntu
    Comment=youdao-dict-for-ubuntu
    Icon=/home/ning/idning-github/youdao-dict-for-ubuntu/icon.png
    Exec=/home/ning/idning-github/youdao-dict-for-ubuntu/dict.py
    Terminal=false
    Type=Application
    OnlyShowIn=GNOME;

实现原理 
========

获取当前选中的单词, 可以使用 ``xclip -o``, 我这里用的是 监听 ``selection_received`` 消息

其它词典
========

- 一个QT版的: https://github.com/lvzongting/youdao-qt
- openyoudao: 比较复杂, python 实现(不错, 不过讨厌网页广告.): 

    - https://github.com/justzx2011/openyoudao
    - http://v.youku.com/v_show/id_XNDAzMDUxNDk2.html

- 此外还有emacs 插件, vim 插件, 命令行版.


`@idning`_

.. _`@idning`: http://weibo.com/idning


