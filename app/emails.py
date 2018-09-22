from flask import render_template, current_app
from flask_mail import Message
from threading import Thread
from app import mail


def async_mail_send(app, msg):                                  # фукция отправляет сообщение в отдельном потоке, требует параметры app и msg
    with app.app_context():                                     # mail.send работает в контексте приложения
        mail.send(msg)


def mail_sender(to, subject, template, **kwargs):
    app = current_app._get_current_object()                     # получить экземпляр текущего приложения
    msg = Message(subject=app.config['RSSREADER_SUBJECT_PREFIX']+subject, sender=app.config['RSSREADER_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)       # добавляем в тело письма текстовую часть
    msg.html = render_template(template+'.html', **kwargs)      # добавляем в тело письма html
    thread = Thread(target=async_mail_send, args=(app, msg))
    thread.start()
    return thread
