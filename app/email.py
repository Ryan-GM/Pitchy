from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject,template,to,**kwargs):
    sender_email = 'monger@gmail.com'
    email = Message(subject,sender = sender_email,receipts = [to])
    email.html = render_template(template + ".html",**kwargs)
    email.body = render_template(template + ".txt",**kwargs)
    mail.send(email)