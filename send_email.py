#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib

from jinja2 import Template

import labevents

import locale
locale.setlocale(locale.LC_ALL, b'en_US.UTF-8')

if __name__ == "__main__":
    session = labevents.database.Session()
    events = filter(lambda e: e.start_date <= datetime.now()+timedelta(weeks=1),
                    labevents.views.events.__get_events(session))

    email_template = Template(
"""Hallo liebe Mitglieder, Nichtmitglieder und Interessierten!

Diese Woche finden im OpenLab folgende Veranstaltungen statt:
{% for e in events %}
  * "{{e.title}}" am {{e.start_date.strftime("%x")}} um {{e.start_date.strftime("%X")}}{% endfor %}

Eine Gesamtübersicht findest Du unter http://events.openlab-augsburg.de

Es würde uns freuen, wenn Du bei der ein oder anderen Veranstatung vorbeischaust!

Grüße,

Dein OpenLab!
""")
    msg = MIMEText(email_template.render(events=events).encode('utf-8'),
                   'plain', 'UTF-8')
    msg['Subject'] = "Die nächste Woche im OpenLab Augsburg"
    msg['From'] = "donotreply@openlab-augsburg.de"
    msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    s = smtplib.SMTP('weltraumpflege.org')
    s.sendmail('donotreply@openlab-augsburg.de', 
               ['stupid@example.com'], 
               msg.as_string())
    s.quit()
