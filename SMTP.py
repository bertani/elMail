#!/usr/bin/env python

 ########################################################################
#                                                                         #
#    This code is written by Thomas Bertani <sylar@anche.no>              #
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

import smtplib

class smtp:
    config = {'email': 'John Doe <email@domain.com>', 'server': 'mail.domain.com', 'username': 'user', 'password': 'passwd'}
    def __init__(self):
        self.server = smtplib.SMTP(self.config['server'])
        self._login()
    def _login(self): self.server.login(self.config['username'], self.config['password'])
    def send(self, to, subject, text):
        from_ = self.config['email']
        msg = "From: %s\r\nTo: %s\r\nMIME-Version: 1.0\r\nSubject: %s\r\nContent-type: text/plain\r\n\r\n%s" % (from_, to, subject, text)
        self.server.sendmail(from_, to, msg)
    def __del__(self): self.server.quit()
