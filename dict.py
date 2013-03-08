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

import youdao_client


g_last_selection = ''

class Dict:
    def get_stringtarget(self, widget):
        ret = widget.selection_convert("PRIMARY", "STRING")
        return True

    def selection_received(self, widget, selection_data, data):
        global g_last_selection
        if str(selection_data.type) == "STRING":
            text = selection_data.get_text()
            if (not text) or (text == g_last_selection): 
                return False
            
            print "STRING TARGET: %s" % selection_data.get_text()

            g_last_selection = text
            word = text.strip().split() [0]
            if len(word) > 20: 
                return 
            if word:
                js = youdao_client.query(word)
                if 'basic' not in js:
                    return 

                youdao_client.pronounce(word)
                #self.window.show()
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
                self.view.show()
                self.view.reload()

        return False

    def __init__(self):
        # Create the toplevel window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Get Selection")
        self.window.set_border_width(10)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.resize(360, 200)

        vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        vbox.show()

        # Create a button the user can click to get the string target
        button = gtk.Button("Get String Target")
        eventbox = gtk.EventBox()
        #eventbox.add(button)
        button.connect_object("clicked", self.get_stringtarget, eventbox)
        eventbox.connect("selection_received", self.selection_received)


        gobject.timeout_add(500, self.get_stringtarget, eventbox)
        import webkit
        self.view = webkit.WebView()
        html = "<h1>Hello!</h1>"
        self.view.load_html_string(html, '')
        self.view.show()
        eventbox.add(self.view)

        vbox.pack_start(eventbox)
        eventbox.show()
        #button.show()

        #window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Dict()
    main()

