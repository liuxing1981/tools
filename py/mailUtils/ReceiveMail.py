import email
import os
from email.header import decode_header
import chardet
from idna import unicode
from imapclient import IMAPClient
from .Criteria import Criteria
from .Mail import Mail


def parseMail(msgdict,attachment_save_path):
    mails,to, mail_content = [], [], ''
    for message_id, message in msgdict.items():
        print(message_id)
        message = convert(message)
        e = email.message_from_string(message['BODY[]'])
        try:
            subject = email.header.make_header(email.header.decode_header(e['SUBJECT']))
            print(subject)
            mail_from = email.header.make_header(email.header.decode_header(e['From']))
            date = email.header.make_header(email.header.decode_header(e['Date']))
            if e['To']:
                to = email.header.make_header(email.header.decode_header(e['To']))
        except Exception:
            pass
        maintype = e.get_content_maintype()
        attachments = []
        if maintype == 'multipart':
            for part in e.walk():
                if part.get_content_maintype() == 'text':
                    mail_content = part.get_payload(decode=True).strip()
                elif part.get_content_maintype() == 'application':
                    data = part.get_payload(decode=True)
                    name = part.get_param("name")
                    if name:
                        file_name = get_part_filename(part)
                        file_name = os.path.join(attachment_save_path, file_name)
                        attachments.append(file_name)
                        with open(file_name, 'wb') as f:
                            f.write(data)
        elif maintype == 'text':
            mail_content = e.get_payload(decode=True).strip()
        try:
            if isinstance(mail_content, bytes):
                # print(mail_content)
                encode = chardet.detect(mail_content)['encoding']
                print(encode)
                if encode.upper() == 'GB2312':
                    encode = 'gbk'
                mail_content = mail_content.decode(encode)
        except UnicodeDecodeError as e:
            print('decode error: try to use unicode')
            print(e)
            mail_content = unicode(mail_content, errors='replace')
            # sys.exit(1)
        else:
            mail = Mail()
            mail.From = mail_from
            mail.Subject = subject
            mail.To = to
            mail.Date = date
            if attachments:
                mail.attachments = attachments
            mail.Content = mail_content
            mail.uid = message_id
            if encode:
                mail.charset = encode
            mails.append(mail)
    return mails


def get_part_filename(part):
    filename = part.get_filename()
    if decode_header(filename)[0][1] is not None:
        filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
    filename = filename.replace('\r','').replace('\n','')
    return filename

def convert(data):
    if isinstance(data, bytes):  return unicode(data, errors='replace')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data

class ImapClient(IMAPClient):
    client = None
    def __init__(self,socket,username,password, attachment_save_path = '.'):
        self.server, self.port = socket.split(':')
        self.port = int(self.port)
        self.username = username
        self.password = password
        self.attachment_save_path = attachment_save_path
        if not os.path.exists(attachment_save_path):
            os.makedirs(attachment_save_path)
        self.mails = []
        if self.client is None:
            ssl = False
            if self.port == 993:
                ssl = True
            super(ImapClient, self).__init__(self.server, self.port, ssl=ssl)
            self.login(self.username, self.password)

    def select_folders(self, folder='INBOX'):
        return self.select_folder(folder,readonly=True)

    def executeQuery(self,criteria):
        query = criteria.getQuery()
        print(*query)
        uid =  self.search(query)
        struid = [ str(x) for x in uid ]
        uid = ','.join(struid)
        msgdict = self.fetch(uid, ['BODY.PEEK[]'])
        return parseMail(msgdict,self.attachment_save_path)

    def queryByUid(self,uid):
        msgdict = self.fetch(uid, ['BODY.PEEK[]'])
        return parseMail(msgdict, self.attachment_save_path)

    def __str__(self):
        for mail in self.mails:
            print(mail)


if __name__=='__main__':
    with ImapClient('imap.qq.com:993','lx_figo','tqtxqntqqrndjgid','e:\\qq_attach') as client:
        client.select_folders()
        criteria = Criteria()
        query1 = criteria.findBySenders('service')
        query2 = criteria.findByDateFrom('2019-12-17')
        criteria.addAnd(query1)
        criteria.addAnd(query2)
        mails = client.executeQuery(criteria)
        # mails = client.queryByUid('448')
        for mail in mails:
            print(mail)
