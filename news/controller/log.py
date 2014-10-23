uthor__ = 'yuan'
#encoding=utf8
from news import app
import news.config as config



if not app.debug:
    import logging
    from logging.handlers import SMTPHandler,RotatingFileHandler
    from logging import Formatter

    #报错邮件
    mailhost=(config.MailHost,config.MailPort)
    credentials=(config.MailUser,config.MailPass)
    mail_handler=SMTPHandler(mailhost=mailhost,fromaddr=config.MailAddr,toaddrs=config.Admin,subject="应用发生错误",credentials=credentials)
    mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s
        Message:            %(message)s
    '''))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


    #日志文件
    file_handler=RotatingFileHandler(filename=config.logPath,mode="a",maxBytes=1*1024*1024,backupCount=10)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)

