from distutils.core import setup
from setuptools import find_packages

setup(name="mailUtils",
      description="for easy search mail and send mail",
      version="1.0",
      author="luis liu",
      author_email="xing.1.liu@nokia-sbell.com",
      license="MIT Licence",
      packages=find_packages(),
      install_requires=['imapclient'],
      py_modules=['__init__', 'Criteria', 'Mail', 'MailServer', 'ReceiveMail', 'SendMail'])
