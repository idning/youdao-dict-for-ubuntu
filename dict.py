#!/usr/bin/env python
#coding: utf-8
#author : ning
#date   : 2013-03-08 21:16:14
'''
timer
'''

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import re
import youdao_client


g_last_selection = ''

class Dict:
    def _on_timer(self, widget):
        print 'on_timer'
        ret = widget.selection_convert("PRIMARY", "STRING")

        #if pop_up_show && distance (xxx): 
            #hide;
        if self.window.get_property('visible'): 
            x, y = self.window.get_position()
            px, py, mods = self.window.get_screen().get_root_window().get_pointer()
            if (px-x)*(px-x) + (py-y)*(py-y) > 400:  # distance > 20 in x, 20 in y
                self.window.hide();

        return True

    def _on_selection_received(self, widget, selection_data, data):
        global g_last_selection
        if str(selection_data.type) == "STRING":
            text = selection_data.get_text()
            if(len(text) > 20):
                return False

            if (not text) or (text == g_last_selection): 
                return False
            
            print "Selected String: %s" % selection_data.get_text()
            g_last_selection = text

            #word = text.strip().split() [0]
            m = re.search(r'[a-zA-Z-]+', text) # the selection mostly be: "widget,", "&window" ... 
            if m :
                word = m.group(0)
                print "Query Word: %s" % word
                self.query_word(word)
            else:
                print "Query nothing"

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
        <h2> %s  <span style="color: #A0A0A0; font-size: 15px">[ %s ] </span> </h2>
        <b>基本翻译:</b>
        <p> %s </p>
        <b>网络释意:</b>
        <p> %s </p>

        ''' % (translation, phonetic, explains, web)
             
        self.view.load_html_string(html, '')
        self.view.reload()

    def __init__(self):
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

    def _on_mouse_leave(self, *args):
        print '_on_mouse_leave'
        self.window.hide()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Dict()
    main()

