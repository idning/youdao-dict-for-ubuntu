#!/usr/bin/env python
#coding: utf-8
#author : ning
#date   : 2013-03-08 21:16:14
'''
timer
'''

import os
import re
import time

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import youdao_client

g_last_selection = ''

PWD = os.path.dirname(os.path.realpath(__file__))
WHITELIST = set( [s.strip() for s in file(PWD + '/common_words.txt').readlines()])

class Dict:
    def _on_timer(self, widget):
        print 'on_timer'
        ret = widget.selection_convert("PRIMARY", "STRING")

        #if pop_up_show && distance (xxx): 
            #hide;
        if self.window.get_property('visible') and not self.mouse_in: 
            x, y = self.window.get_position()
            px, py, mods = self.window.get_screen().get_root_window().get_pointer()
            if (px-x)*(px-x) + (py-y)*(py-y) > 400:  # distance > 20 in x, 20 in y
                print 'distance big enough, hide window '
                self.window.hide();
            if(time.time() - self.popuptime > 3):   # popup for some seconds
                print 'time long enough, hide window '
                self.window.hide();

        return True

    def _on_selection_received(self, widget, selection_data, data):
        global g_last_selection
        if str(selection_data.type) == "STRING":
            text = selection_data.get_text()
            text = text.decode('raw-unicode-escape')
            if(len(text) > 20):
                return False

            if (not text) or (text == g_last_selection): 
                return False
            
            print "Selected String: %s" % text
            
            print `text`
            g_last_selection = text

            #word = text.strip().split() [0]
            m = re.search(r'[a-zA-Z-]+', text.encode('utf8')) # the selection mostly be: "widget,", "&window" ... 
            if not m: 
                print "Query nothing"
                return False

            word = m.group(0).lower()
            if self.ignore(word):
                print 'Ignore Word: ', word
                return False

            print "Query Word: ",  word
            self.query_word(word)

        return False

    def ignore(self, word):
        if len(word)<=3:
            return True
        if word in WHITELIST: 
            return True
        return False

    def query_word(self, word):
        js = youdao_client.query(word)
        if 'basic' not in js:
            return 

        youdao_client.pronounce(word)
        x, y, mods = self.window.get_screen().get_root_window().get_pointer()
        self.window.move(x+15, y+10)

        self.window.present()

        translation = '<br/>'.join(js['translation']) 
        if 'phonetic' in js['basic']:
            phonetic = js['basic']['phonetic']
        else:
            phonetic = ''
        explains = '<br/>'.join(js['basic']['explains']) 
        #web = '<br/>'.join( ['<a href="http://dict.youdao.com/search?le=eng&q=%s">%s</a>: %s'%(i['key'], i['key'], ' '.join(i['value'])) for i in js['web'][:3] ] )
        web = '<br/>'.join( ['<a href="">%s</a>: %s'%(i['key'], ' '.join(i['value'])) for i in js['web'][:3] ] )
        html = '''
        <h2> 
        %s  
        <span style="color: #A0A0A0; font-size: 15px">[ %s ] </span> 
        <span style="color: #0B6121; font-size: 12px">< %s > </span> 
        </h2>
        
        <b>基本翻译:</b>
        <p> %s </p>
        <b>网络释意:</b>
        <p> %s </p>

        ''' % (translation, phonetic, word, explains, web)
                   
        self.view.load_html_string(html, '')
        self.view.reload()
        self.popuptime = time.time()

    def __init__(self):
        self.mouse_in = False

        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.set_title("youdao-dict-for-ubuntu")
        self.window.set_border_width(3)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.resize(360, 200)

        vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        vbox.show()

        eventbox = gtk.EventBox()

        eventbox.connect("selection_received", self._on_selection_received)
        eventbox.connect('enter-notify-event', self._on_mouse_enter)
        eventbox.connect('leave-notify-event', self._on_mouse_leave)

        gobject.timeout_add(500, self._on_timer, eventbox)

        import webkit
        self.view = webkit.WebView()
        html = "<h1>Hello!</h1>"
        self.view.load_html_string(html, '')
        self.view.show()
        eventbox.add(self.view)

        vbox.pack_start(eventbox)
        eventbox.show()

    def _on_mouse_enter(self, wid, event):
        print '_on_mouse_enter'
        self.mouse_in = True

    def _on_mouse_leave(self, *args):
        print '_on_mouse_leave'
        self.mouse_in = False
        self.window.hide()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Dict()
    main()

