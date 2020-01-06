from distutils.core import setup

setup(name="mailUtils",
      description="for easy search mail and send mail",
      version="1.0",
      author="luis liu",
      author_email="xing.1.liu@nokia-sbell.com",
      py_modules=['__init__', 'Criteria','Mail','MailServer','ReceiveMail','SendMail'],
      install_requires=['imapclient'])