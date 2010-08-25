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

import poplib, email, mimetypes

class Protocol:
    config = {'server': 'mail.domain.com', 'username': 'user', 'password': 'passwd'}
    def __init__(self): pass
    def _login(self):
        self.server = poplib.POP3(self.config['server'])
        try:
            self.server.user(self.config['username'])
            self.server.pass_(self.config['password'])
        except poplib.error_proto:
            return False
        else:
            return True
    def _list_count(self):
        #ritorna il numero di messaggi sul server
        return self.server.stat()[0]
    def _get_message(self, n):
        message = email.message_from_string('\r\n'.join(self.server.retr(n+1)[1]))
        from_ = message["From"]
        subject = message["Subject"]
        date = message["Date"]
        for i in message.walk():
            if i.get_content_maintype() == 'text': text = i.get_payload(decode=True)
        return (1, {"id": n, "from": from_, "subject": subject, "text": text, "date": date})

if __name__ == '__main__':
    backend = Protocol()
    print backend._login()
    for i in range(backend._list_count()): print backend._get_message(i)
