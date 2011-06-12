import smtplib
import string, sys

import db

HOST = "localhost"

FROM = "bugdb@iesedev.org"


def emailUser(subject, body_text, toList):
    
    for to in toList:
        body = string.join(("From: %s" % FROM, "To: %s" % to, "Subject: %s" % subject,"",body_text), "\r\n")
        
        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, [to], body)
        server.quit()




def bugAssignNotify(bugh, to):

    subject = '[Sev '+str(bugh['priority'])+'] '+'Bug '+str(bugh['bug_id'])+' has been assigned to you'

    body_text = """Bug Title: """+bugh['title'] \
        +"""\nCustomer: """+bugh['customer'] \
        +"""\nPriority: """+bugh['priority'] \
        +"""\nDescription: """+bugh['description'] \
        +"""\n """

    emailUser(subject, body_text, to)
    
    
