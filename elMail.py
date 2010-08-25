#!/usr/bin/env python

 ########################################################################
#                                                                         #
#    This code is written by Thomas Bertani <thomas.bertani@nesit.it>     #
#    Copyright (C) 2010 Nesit - Via Savelli 128, 35129 Padova, ITALY      #
#                                                                         #
#    This file is part of elMail.                                         #
#                                                                         #
#    elMail is free software: you can redistribute it and/or modify       #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 2 of the License, or    #
#    (at your option) any later version.                                  #
#                                                                         #
#    elMail is distributed in the hope that it will be useful,            #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
#    GNU General Public License for more details.                         #
#                                                                         #
#    You should have received a copy of the GNU General Public License    #
#    along with elMail.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                         #
 #########################################################################

import gettext
import ecore, elementary
from functools import partial
from backend import Backend

class eMail:
    ver = "0.4b"
    win_title = "eMail v%s" % ver
    mode = ""
    def _message(self, msg="", timeout=5):
        def inwin_close(*args, **kwarks):
            self.innerWin.hide()
            self.innerWinAnchor.hide()
        inwin_close()
        if not msg: return
        self.innerWin.content_set(self.innerWinAnchor)
        self.innerWinAnchor.text_set(self.__to_html(msg))
        self.innerWin.activate()
        if timeout!=-1: ecore.timer_add(timeout, inwin_close)
    def composeNew(self, *args, **kwargs):
        _to = kwargs.get("_to", _("email@domain.com"))
        _subject = kwargs.get("_subject", _("Subject!"))
        def _send(*args, **kwargs):
            self.backend.send(to_entry.entry_get(), subject_entry.entry_get(), text_entry.entry_get())
            inwin_close()
        def inwin_close(*args, **kwargs): innerWin.hide()
        innerWin = elementary.InnerWindow(self.win)
        innerMainBox = elementary.Box(innerWin)
        innerMainBox.size_hint_weight_set(1.0, 1.0)
        innerMainBox.size_hint_align_set(-1.0, -1.0)
        innerBox = elementary.Box(innerWin)
        
        def select_all(*args, **kwargs):
            args[0].select_all()
        to_entry = elementary.Entry(innerWin)
        to_entry.on_mouse_down_add(select_all)
        to_entry.single_line_set(True)
        to_entry.entry_set(_to)
        to_entry.show()
        subject_entry = elementary.Entry(innerWin)
        subject_entry.on_mouse_down_add(select_all)
        subject_entry.single_line_set(True)
        subject_entry.entry_set(_subject)
        subject_entry.show()
        text_entry = elementary.Entry(innerWin)
        text_entry.on_mouse_down_add(select_all)
        text_entry.entry_set(_("Insert here the email's text"))
        text_entry.show()
        innerBox.pack_end(to_entry)
        innerBox.pack_end(subject_entry)
        innerBox.pack_end(text_entry)
        
        innerBox.size_hint_weight_set(1.0, 1.0)
        innerBox.size_hint_align_set(-1.0, -1.0)
        btns = elementary.Box(innerWin)
        btns.horizontal_set(True)
        btns.size_hint_align_set(-1.0, -1.0)
        send_btn = elementary.Button(innerWin)
        send_btn._callback_add('clicked', _send)
        send_btn.size_hint_weight_set(1.0, 1.0)
        send_btn.size_hint_align_set(-1.0, -1.0)
        send_btn.label_set(_("Send"))
        close_btn = elementary.Button(innerWin)
        close_btn._callback_add('clicked', inwin_close)
        close_btn.size_hint_weight_set(1.0, 1.0)
        close_btn.size_hint_align_set(-1.0, -1.0)
        close_btn.label_set(_("Close"))
        btns.pack_end(send_btn)
        btns.pack_end(close_btn)
        innerMainBox.pack_end(innerBox)
        innerMainBox.pack_end(btns)
        innerWin.content_set(innerMainBox)
        innerMainBox.show()
        innerBox.show()
        send_btn.show()
        close_btn.show()
        btns.show()
        innerWin.activate()
    def __init__(self):
        self.backend = Backend()
    def __to_html(self, msg):
        msg = msg.replace("\n", "<br>")
        msg = msg.replace("\r", "")
        msg = msg.replace("<br/>", "<br>")
        return msg
    def _change_mode(self, mode, *args, **kwargs):
        if self.mode == mode: return
        self.mode = mode
        self._mainList_populate()
    def _show_messages(self, email_list, *args, **kwargs):
        innerWin = elementary.InnerWindow(self.win)
        innerMainBox = elementary.Box(innerWin)
        innerMainBox.size_hint_weight_set(1.0, 1.0) 
        innerMainBox.size_hint_align_set(-1.0, -1.0) 
        innerScroller = elementary.Scroller(innerWin)
        innerScroller.bounce_set(0, 1)
        innerScroller.size_hint_weight_set(1.0, 1.0)
        innerScroller.size_hint_align_set(-1.0, -1.0)
        innerBox = elementary.Box(innerWin)
        innerBox.size_hint_weight_set(1.0, 1.0)
        innerBox.size_hint_align_set(-1.0, -1.0)
        for i in email_list:
            msg = self.backend._get_message(i)
            b = elementary.Bubble(innerBox)
            b.size_hint_weight_set(1.0, 0.0)
            b.size_hint_align_set(-1.0, -1.0)
            mittente = msg['from'] if not msg['from'].find("<") else msg['from'][:msg['from'].find("<")]
            b.label_set("%s [%s]" % (mittente, msg['short_date']))
            text = elementary.AnchorBlock(self.innerWin)
            text.text_set(self.__to_html(msg['text']))
            text.size_hint_weight_set(1.0, 0.0)
            text.size_hint_align_set(-1.0, -1.0)
            b.content_set(text)
            b.show()
            innerBox.pack_end(b)
        innerScroller.content_set(innerBox)
        innerScroller.show()
        innerBox.show()
        innerMainBox.pack_end(innerScroller)
        btns_box = elementary.Box(innerWin)                                  
        btns_box.horizontal_set(True)                                        
        btns_box.homogenous_set(True)                                           
        btns_box.size_hint_align_set(-1.0, -1.0)                             
        cls_btn = elementary.Button(innerWin)                                
        def inwin_close(*args, **kwarks):                                    
            innerWin.hide()                                                  
        cls_btn.size_hint_weight_set(1.0, 1.0)                               
        cls_btn.size_hint_align_set(-1.0, -1.0)                              
        cls_btn.label_set(_("Close"))                                          
        cls_btn._callback_add('clicked', inwin_close)                        
        cls_btn.show()                                                       
        reply_btn = elementary.Button(innerWin)                              
        def reply(*args, **kwarks):                                          
            inwin_close()        
            _from = msg['from']
            _from = _from if not _from.find("<") else _from[_from.find("<")+1:-1]                                            
            _subject = msg['subject']
            self.composeNew(_to=_from, _subject="Re: %s" % _subject)         
        reply_btn.size_hint_weight_set(1.0, 1.0)                             
        reply_btn.size_hint_align_set(-1.0, -1.0)                            
        reply_btn.label_set("Rispondi")                                      
        reply_btn._callback_add('clicked', reply)                            
        reply_btn.show()                                                     
        btns_box.pack_end(reply_btn)                                         
        btns_box.pack_end(cls_btn)
        btns_box.show() 
        innerMainBox.pack_end(btns_box)
        innerMainBox.show()
        innerWin.content_set(innerMainBox)                                           
        innerWin.activate()                                                
    def _mainList_populate(self):
        filter = self.mode
        self.mainList.clear()
        if filter=="author":
            messages = self.backend._get_list(order_by="author")
            authors = messages.keys()
            authors.sort()
            for author in authors:
                email_list = []
                for message in messages[author]:
                    email_list.append(message['id'])
                self.mainList.item_append(author, None, None, partial(self._show_messages, email_list))
        elif filter=="thread":
            messages = self.backend._get_list(order_by="thread")
            threads = messages.keys()
            threads.sort()
            for thread in threads:
                email_list = []
                for message in messages[thread]:
                    email_list.append(message['id'])
                self.mainList.item_append(thread, None, None, partial(self._show_messages, email_list))
        else:
            for message in self.backend._get_list(order_by=""):
                self.mainList.item_append("[%s] %s" % (message['from'], message['subject']), None, None, partial(self._show_messages, (message['id'],))) 
        self.mainList.go()
    def sync(self, *args, **kwargs):
        self._message(_("Checking your inbox for new emails.."))
        ecore.timer_add(0.1, self.sync_init)
    def sync_init(self, *args, **kawargs):
        self.backend.sync_stepbystep_init()
        if self.backend.syncronizing: self.sync_nextstep()
        self._message()
    def sync_nextstep(self, *args, **kwargs):
        if self.backend.syncronizing:
            status = self.backend.sync_next()
            self._message("%s<br><br><br>%s <a href=''>%s</a> %s <a href=''>%s</a>" % (_("Sync"), _("Emails retrieved:"), status[0], _("of"), status[1]))
            ecore.timer_add(0.1, self.sync_nextstep)
        else:
            self._mainList_populate()
            self._message()
    def quit(self, obj, event, data):
        elementary.exit()
    def initUi(self):
        self.win = elementary.Window(self.win_title, elementary.ELM_WIN_BASIC)
        self.win.title_set(self.win_title)
        self.win.callback_destroy_add(self.quit, None, None)
        ##
        self.innerWin = elementary.InnerWindow(self.win)
        self.innerWin.size_hint_weight_set(1.0, 1.0)
        self.innerWin.size_hint_align_set(-1.0, -1.0)
        self.innerWinAnchor = elementary.AnchorView(self.innerWin)
        ##
        self.bg = elementary.Background(self.win)
        self.bg.size_hint_weight_set(1.0, 1.0)
        ##
        self.mainBox = elementary.Box(self.win)
        self.mainBox.size_hint_weight_set(1.0, 1.0)
        ##
        self.mainFrame = elementary.Frame(self.win)
        self.mainFrame.size_hint_weight_set(1.0, 1.0)
        self.mainFrame.size_hint_align_set(-1.0, -1.0)
        self.mainFrame.label_set(self.win_title)
        ##
        self.mainList = elementary.List(self.win)
        self.mainList.size_hint_weight_set(1.0, 1.0)
        self.mainList.size_hint_align_set(-1.0, -1.0)
        self._mainList_populate()
        ##
        self.filterSelector = elementary.Hoversel(self.win)
        self.filterSelector.label_set(_("Show emails ordered by"))
        self.filterSelector.hover_parent_set(self.win)
        self.filterSelector.size_hint_weight_set(1.0, -1.0)
        self.filterSelector.size_hint_align_set(-1.0, -1.0)
        self.filterSelector.item_add(_("ordered by date"), "", elementary.ELM_ICON_NONE, partial(self._change_mode, ""))
        self.filterSelector.item_add(_("grouped by author"), "", elementary.ELM_ICON_NONE, partial(self._change_mode, "author"))
        self.filterSelector.item_add(_("grouped by thread"), "", elementary.ELM_ICON_NONE, partial(self._change_mode, "thread"))
        ##
        self.frameBox = elementary.Box(self.win)
        self.frameBox.size_hint_weight_set(1.0, 1.0)
        self.frameBox.pack_end(self.filterSelector)
        self.frameBox.pack_end(self.mainList)
        ##
        self.newButton = elementary.Button(self.win)
        self.newButton.label_set(_("New"))
        self.newButton._callback_add('clicked', self.composeNew)
        self.newButton.size_hint_weight_set(1.0, 1.0)
        self.newButton.size_hint_align_set(-1.0, -1.0)
        self.syncButton = elementary.Button(self.win)
        self.syncButton.label_set(_("Sync Inbox"))
        self.syncButton._callback_add('clicked', self.sync)
        self.syncButton.size_hint_weight_set(1.0, 1.0)
        self.syncButton.size_hint_align_set(-1.0, -1.0)
        self.actionsBox = elementary.Box(self.win)
        self.actionsBox.horizontal_set(True)
        self.actionsBox.homogenous_set(True)
        #self.actionsBox.size_hint_weight_set(1.0, 1.0)
        self.actionsBox.size_hint_align_set(-1.0, -1.0)
        self.actionsBox.pack_end(self.newButton)
        self.actionsBox.pack_end(self.syncButton)
        ##
        self.mainFrame.content_set(self.frameBox)
        self.mainBox.pack_end(self.mainFrame)
        self.mainBox.pack_end(self.actionsBox)
        self.win.resize_object_add(self.bg)
        self.win.resize_object_add(self.mainBox)
        self.win.resize_object_add(self.innerWin)
        ##  
        self.bg.show()
        self.mainBox.show()
        self.mainFrame.show()
        self.frameBox.show()
        self.filterSelector.show()
        self.mainList.show()
        self.actionsBox.show()
        self.newButton.show()
        self.syncButton.show()
        self.win.show()
if __name__ == '__main__':
    gettext.install("elMail", "./")
    main = eMail()
    elementary.init()
    elementary.scale_set(1.5)
    main.initUi()
    elementary.run()
    elementary.shutdown()
