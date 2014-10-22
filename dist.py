#!/usr/bin/env python
#coding: utf-8
#file   : dist.py
#author : ning
#date   : 2014-10-22 17:24:23


import subprocess
import time

def system(cmd, log=True):
    subprocess.Popen(cmd, shell=True)

def create_file(path, exe, content):
    f = file(path, 'w')
    f.write(content)
    f.close()
    if exe:
        system('chmod +x %s' % path)

system('mkdir -p dist/youdao-dict/DEBIAN')
system('mkdir -p dist/youdao-dict/usr/bin')
system('mkdir -p dist/youdao-dict/usr/share')
system('mkdir -p dist/youdao-dict/usr/share/applications')
system('mkdir -p dist/youdao-dict/etc/xdg/autostart')

time.sleep(.1)

system('cp -r youdao_dict dist/youdao-dict/usr/share')

create_file('dist/youdao-dict/usr/bin/youdao-dict', True, '''
/usr/bin/python /usr/share/youdao_dict/dict.py
''')

create_file('dist/youdao-dict/DEBIAN/control', False, '''
Package: youdao-dict
Version: 0.1.0
Maintainer: ning <idning@gmail.com>
Architecture: all
Depends: python, python-gtk2, python-webkit, mplayer
Description: youdao dict for ubuntu
''')

create_file('dist/youdao-dict/usr/share/applications/youdao-dict.desktop', False, '''
[Desktop Entry]
Name=Youdao-dict-for-ubuntu
Comment=youdao-dict-for-ubuntu
Icon=/usr/share/youdao_dict/icon.png
Exec=/usr/bin/youdao-dict
Terminal=false
Type=Application
Categories=Office;
MimeType=application/xmind;
''')

system('cp dist/youdao-dict/usr/share/applications/youdao-dict.desktop dist/youdao-dict/etc/xdg/autostart')

system('dpkg --build dist/youdao-dict/ dist/youdao-dict-0.1.0_all.deb')

#install
system('dpkg -i dist/youdao-dict-0.1.0_all.deb')
