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

import imaplib, email, mimetypes

class Protocol:
    config = {'server': 'mail.domain.com', 'username': 'user', 'password': 'passwd'}
    def __init__(self): pass
    def _login(self):
        self.server = imaplib.IMAP4(self.config['server'])
        try:
            self.server.login(self.config['username'], self.config['password'])
            self.server.select()
        except imaplib.IMAP4.error:
            return False
        else:
            return True
    def _list_count(self):
        #ritorna il numero di messaggi sul server
        status, data = self.server.search(None, 'ALL')
        data = data[0].split()
        return len(data)
    def _get_message(self, n):
        def get_field(message, field):
            res = ""
            for line in str(message).split("\n"):
                if line.startswith(field+":"): res = line[len(field)+2:-1]
            return res
        msg = self.server.fetch(n, '(RFC822)')[1][0][1]
        message = email.message_from_string(msg)
        from_ = message["From"] if message["From"] else get_field(message, "From")
        subject = message["Subject"] if message["Subject"] else get_field(message, "Subject")
        date = message["Date"] if message["Date"] else get_field(message, "Date")
        text = ""
        for n_, line in enumerate(str(message).split("\n")):
            if line.find(": text/plain") != -1:
                for line in str(message).split("\n")[n_+1:]:
                    if line.startswith("Content-Type") or line.startswith("--"): break
                    if line.startswith("Content-") or line.find("Date:") != -1 or line.startswith("Message-Id:") or line.startswith("Subject:"): continue
                    text += line+"\n"
                break
        #for i in message.walk():
        #    if i.get_content_maintype() == 'text': text = i.get_payload(decode=True)
        return (1, {"id": n, "from": from_, "subject": subject, "text": text, "date": date})

if __name__ == '__main__':
    backend = Protocol()
    print backend._login()
    for i in range(backend._list_count()): print backend._get_message(i)
