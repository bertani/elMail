#!/usr/bin/env python

 ########################################################################
#                                                                         #
#    Copyright (C) 2010 Thomas Bertani <sylar@anche.no>                   #
#                                                                         #
#    This file is part of elMail.                                         #
#                                                                         #
#    elMail is free software: you can redistribute it and/or modify       #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 3 of the License, or    #
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

from sqlite3 import dbapi2 as sqlite
from IMAP import Protocol

from SMTP import smtp

class Backend:
    db_file = "email.db"
    def _db_init(self):
        try:
            self.db_cursor.execute("CREATE TABLE email (id INTEGER PRIMARY KEY, date VARCHAR(50), `from` VARCHAR(50), subject VARCHAR(100), text VARCHAR(500))")
            self.db_connection.commit()
        except: pass
    def __init__(self):
        self.db_connection = sqlite.connect(self.db_file)
        self.db_connection.text_factory = str
        self.db_cursor = self.db_connection.cursor()
        self._db_init()
    def sync_stepbystep_init(self):
        self.from_ = self._get_lastemail_number()
        self.protocol = Protocol()
        self.protocol._login()
        self.to = self.protocol._list_count()
        self.current = self.from_ + 1
        if (self.to - self.from_)>0: self.syncronizing = True
        else: self.syncronizing = False
    def sync_next(self):
        self._store_message(self.protocol._get_message(self.current)[1])
        self.db_connection.commit()
        self.current += 1
        if self.current > self.to:
            #self.db_connection.commit()
            self.syncronizing = False
        return (self.current - 1, (self.to-self.from_))
    def send(self, to, subject, text):
        smtp().send(to, subject, text)
    def sync(self):
        protocol = Protocol()
        protocol._login()
        from_ = self._get_lastemail_number()
        to = protocol._list_count()
        for n in range(from_+1, to+1):
            self._store_message(protocol._get_message(n)[1])
        self.db_connection.commit()
        return {'new': {'inbox': (to-from_)}}
    def _get_lastemail_number(self):
        self.db_cursor.execute("SELECT max(id) FROM email")
        max_id = self.db_cursor.fetchall()[0][0]
        if not max_id: max_id = 0
        return max_id
    def _store_message(self, message):
        self.db_cursor.execute("INSERT INTO email VALUES (?, ?, ?, ?, ?)", (message['id'], message['date'], message['from'], message['subject'], message['text']))
        return True
    def _get_message(self, n):
        from time import strftime, strptime
        self.db_cursor.execute("SELECT * FROM email WHERE id=%s" % n)
        row = self.db_cursor.fetchone()
        if row[1]:
            d = strptime(row[1], "%a, %d %b %Y %H:%M:%S +0200")
            date_ = strftime("%H:%M.%S %d.%m.%Y", d)
            short_date = strftime("%H.%M.%S %d.%m.%y", d)
        else: date_, short_date = "???", "???"
        return {'id': row[0], 'date': date_, 'short_date': short_date, 'from': row[2], 'subject': row[3], 'text': row[4]}
    def _get_list(self, order_by="simple"):
        if order_by == "simple": return self._get_list_simple()
        elif order_by == "author": return self._get_list_by_author()
        elif order_by == "thread": pass
        return self._get_list_simple()
    def _get_list_by_author(self):
        self.db_cursor.execute("SELECT * FROM email")
        list = {}
        for row in self.db_cursor:
            message = {'id': row[0], 'date': row[1], 'from': row[2], 'subject': row[3], 'text': row[4]}
            if not list.has_key(message['from']): list[message['from']] = []
            list[message['from']].append(message)
        return list
    def _get_list_simple(self):
        self.db_cursor.execute("SELECT * FROM email")
        list = []
        for row in self.db_cursor:
            message = {'id': row[0], 'date': row[1], 'from': row[2], 'subject': row[3], 'text': row[4]}
            list.append(message)
        return list
