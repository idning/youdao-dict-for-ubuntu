
当前ubuntu下的字典
==================

:stardict: 
   StarDict hasn't seen any active development for many years
   推荐 GoldenDict
:GoldenDict: 
   确实不错, 但是占CPU. 常年占20%
:youdao:
    网页版而且有广告.
    chrome 插件不错. 

stardict, GoldenDict 的一个共同问题是, 查询结果的字体都是一样大小. 很不好看.

特点: 
=====

1. 自动取词, 鼠标跟随
2. 发音.
3. 单词白名单
4. 用chrome 浏览器跳转到youdao查词.

5. 基于web版youdao , 而不是API(http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q=hello)
   因为API 通常有鉴权而比较慢.

.. image:: https://raw.github.com/idning/youdao-dict-for-ubuntu/master/imgs/youdao-dict.png
    :height: 355px

实现
====

获取当前选中的单词, 可以使用 ``xclip -o``, 我这里用的是 监听 ``selection_received`` 消息

install
=======

1. pip install xxx
2. TODO



其它
====

- 一个QT版的: https://github.com/lvzongting/youdao-qt
- openyoudao: 比较复杂, python 实现(不错, 不过讨厌网页广告.): 

    - https://github.com/justzx2011/openyoudao
    - http://v.youku.com/v_show/id_XNDAzMDUxNDk2.html

- 此外还有emacs 插件, vim 插件, 命令行版.


`@idning`_

.. _`@idning`: http://weibo.com/idning

