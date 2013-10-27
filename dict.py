#!/usr/bin/env python
#coding: utf-8
#author : ning
#date   : 2013-03-08 21:16:14

import os
import re
import time
import fcntl 
import logging

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import webkit

import youdao_client

PWD = os.path.dirname(os.path.realpath(__file__))
WHITELIST = set( [s.strip() for s in file(PWD + '/common_words.txt').readlines()])
LOGO = PWD + '/icon.png'

if not os.path.exists(PWD + '/log/'):
    os.mkdir(PWD + '/log/')
log_path = PWD + '/log/dict.log'
logging.basicConfig(filename=log_path, level=logging.DEBUG)

class Dict:
    def __init__(self):
        self.mouse_in = False
        self.popuptime = 0
        self.last_selection = ''

        self.window = None
        self.view = None

        self.init_widgets()

    def init_widgets(self):
        '''
        window->vbox->eventbox->view
        '''
        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.set_title("youdao-dict-for-ubuntu")
        self.window.set_border_width(3)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.resize(360, 200)

        vbox = gtk.VBox(False, 0)
        vbox.show()

        eventbox = gtk.EventBox()
        eventbox.connect("selection_received", self._on_selection_received)
        eventbox.connect('enter-notify-event', self._on_mouse_enter)
        eventbox.connect('leave-notify-event', self._on_mouse_leave)
        gobject.timeout_add(500, self._on_timer, eventbox)
        eventbox.show()

        self.view = webkit.WebView()
        def title_changed(widget, frame, title):
            logging.debug('title_changed to %s, will open webbrowser ' % title)
            import webbrowser
            webbrowser.open('http://dict.youdao.com/search?le=eng&q=' + title )
        self.view.connect('title-changed', title_changed)
        self.view.show()

        #add one by one 
        self.window.add(vbox)
        vbox.pack_start(eventbox) # means add
        eventbox.add(self.view)

    def _on_timer(self, widget):
        '''
        1. Requests the contents of a selection. (will trigger `selection_received`)
        2. hide window if necessary
        '''

        widget.selection_convert("PRIMARY", "STRING")

        #if pop_up_show && distance (xxx): 
            #hide;
        if self.window.get_property('visible') and not self.mouse_in: 
            x, y = self.window.get_position()
            px, py, mods = self.window.get_screen().get_root_window().get_pointer()
            if (px-x)*(px-x) + (py-y)*(py-y) > 400:  # distance > 20 in x, 20 in y
                logging.debug('distance big enough, hide window')
                self.window.hide();
            if(time.time() - self.popuptime > 3):   # popup for some seconds
                logging.debug('time long enough, hide window')
                self.window.hide();

        return True

    def _on_selection_received(self, widget, selection_data, data):
        if str(selection_data.type) == "STRING":
            text = selection_data.get_text()
            if not text:
                return False
            text = text.decode('raw-unicode-escape')
            if(len(text) > 20):
                return False

            if (not text) or (text == self.last_selection): 
                return False
            
            logging.info("======== Selected String : %s" % text)
            self.last_selection = text

            m = re.search(r'[a-zA-Z-]+', text.encode('utf8')) # the selection mostly be: "widget,", "&window" ... 
            if not m: 
                logging.info("Query nothing")
                return False

            word = m.group(0).lower()
            if self.ignore(word):
                logging.info('Ignore Word: ' + word)
                return False

            logging.info('QueryWord: ' + word)
            self.query_word(word)

        return False

    def query_word(self, word):
        js = youdao_client.query(word)
        if 'basic' not in js:
            logging.info('IgnoreWord: ' + word)
            return 
        logging.info('PronounceWord: ' + word)

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
<style>
.add_to_wordbook {
    background: url(http://bs.baidu.com/yanglin/add.png) no-repeat;
    vertical-align: middle;
    overflow: hidden;
    display: inline-block;
    vertical-align: top;
    width: 24px;
    padding-top: 26px;
    height: 0;
    margin-left: .5em;
}
</style>

        <h2> 
        %(translation)s  
        <span style="color: #0B6121; font-size: 12px">< %(phonetic)s > </span> 
        <a href="javascript:void(0);" id="wordbook" class="add_to_wordbook" title="点击在浏览器中打开" onclick="document.title='%(word)s'"></a> <br/>
        </h2>

        <span style="color: #A0A0A0; font-size: 15px">[ %(word)s ] </span> 
        <b>基本翻译:</b>
        <p> %(explains)s </p>

        <span style="color: #A0A0A0; font-size: 15px">[ %(word)s ] </span> 
        <b>网络释意:</b>
        <p> %(web)s </p>

        ''' % locals()
                   
        self.view.load_html_string(html, '')
        self.view.reload()
        self.popuptime = time.time()

    def ignore(self, word):
        if len(word)<=3:
            return True
        if word in WHITELIST: 
            return True
        return False

    def _on_mouse_enter(self, wid, event):
        logging.debug('_on_mouse_enter')
        self.mouse_in = True

    def _on_mouse_leave(self, *args):
        logging.debug('_on_mouse_leave')
        self.mouse_in = False
        self.window.hide()

class DictStatusIcon:
    def __init__(self):
        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_file(LOGO) 
        self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.set_tooltip("StatusIcon Example")
        
        # 这里可以放一个配置界面
        #window = gtk.Window()
        #window.connect("destroy", lambda w: gtk.main_quit())
        #window.show_all()
        
    def right_click_event(self, icon, button, time):
        menu = gtk.Menu()

        itemlist = [(u'About', self.show_about_dialog),
                    (u'Quit', gtk.main_quit)]

        for text, callback in itemlist:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)

        menu.show_all()
        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)
        
    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("youdao-dict-for-ubuntu")
        about_dialog.set_version("0.0.2")
        about_dialog.set_authors(["idning"])
                
        about_dialog.run()
        about_dialog.destroy()

def main():
    DictStatusIcon()
    Dict()
    gtk.main()

if __name__ == "__main__":
    LOCK_F = PWD +  '/.lock'
    f=open(LOCK_F, 'w') 
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB) 
    except:
        print 'a process is already running!!!'
        exit(0)

    main()

