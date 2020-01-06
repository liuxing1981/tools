import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from .MailServer import QQServer
from .Mail import Mail


class SendMail():
    def __init__(self, socket, username, password):
        self.server,self.port = socket.split(':')
        self.port = int(self.port)
        self.username = username
        self.password = password

    def _attachmentMail(self,mail):
        message = MIMEMultipart()
        message['From'] = Header(mail.From, mail.charset)
        message['To'] = Header(mail.To, mail.charset)
        message['Subject'] = Header(mail.Subject, mail.charset)
        message.attach(MIMEText(mail.Content, mail.Type, mail.charset))
        for path in mail.attachments:
            att = MIMEText(open(path, 'rb').read(), 'base64', mail.charset)
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"'%os.path.basename(path)
            message.attach(att)
        return message

    def _textMail(self,mail):
        message = MIMEText(mail.Content, mail.Type, mail.charset)
        message['From'] = Header(mail.From, mail.charset)
        message['To'] = Header(mail.To, mail.charset)
        message['Subject'] = Header(mail.Subject, mail.charset)
        return message

    def send_mail(self, mail):
        if len(mail.attachments) != 0:
            message = self._attachmentMail(mail)
        else:
            message = self._textMail(mail)
        try:
            smtpObj = None
            if self.port == smtplib.SMTP_PORT:
                smtpObj = smtplib.SMTP(self.server,self.port)
            elif self.port == smtplib.SMTP_SSL_PORT:
                smtpObj = smtplib.SMTP_SSL(self.server,self.port)
            # smtpObj.set_debuglevel(1)
            # smtpObj.ehlo()
            # smtpObj.starttls()
            # smtpObj.ehlo
            smtpObj.login(self.username, self.password)
            smtpObj.sendmail(mail.From, mail.To, message.as_string())
            print("send successfully!")
            smtpObj.close()
        except smtplib.SMTPException as e:
            print("Error: mail send failed!")
            print(e)


if __name__=='__main__':
    client = SendMail(QQServer.SMTP,'lx_figo','yvnqivuetaidgbfc')
    mail = Mail()
    mail.From = 'lx_figo@qq.com'
    mail.To = mail.From
    mail.Subject = 'Test mail'
    mail.Content = '''
    Hello world
    This is a test mail
    '''
    mail.attachments = ['e:\\hss.schema.modify.ldif']
    client.send_mail(mail)