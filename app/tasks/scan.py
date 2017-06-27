# -*- coding: utf-8 -*-
import os
import re
import paramiko

from sqlalchemy.orm.exc import NoResultFound
from app.tasks import app
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from app.conf.config import CONFIG
from app.model import DBSession
from app.model.file import File
from app.util.dbutil import *

session = DBSession()
logger = get_task_logger(__name__)
ssh = paramiko.SSHClient()


@app.on_after_configure.connect
def set_up_periodic_tasks(sender, **kwargs):
    # 每10s执行一次任务
    sender.add_periodic_task(10.0, scan.s(), name='scan every 10 seconds')
    sender.add_periodic_task(10.0, check.s(), name='check every 10 seconds')


@app.task(name='app.tasks.scan.scan')
def scan():
    files = os.listdir(CONFIG['DIR_TO_SCAN'])
    for filename in files:
        if not os.path.isdir(CONFIG['DIR_TO_SCAN'] + filename):
            try:
                session.query(File).filter(File.name == filename).one()
                logger.info('old file found, pass')
            except NoResultFound:
                logger.info('new file found, save to db')
                # 正则匹配找到文件中的时间字符串
                logger.debug('123>>>>>')
                file_to_save = File(name=filename, status=1000, date=re.findall(r'\d{8}', filename)[0])
                logger.debug('123>>>>>')
                session.add(file_to_save)
                logger.debug('123>>>>>')
                session.commit()
                trans(filename, '123', '321')
            finally:
                session.close()


@app.task(name='app.tasks.scan.check')
def check():
    results = get_file_to_trans()
    print results
    for result in results:
        trans(result.name)


# sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
def trans(filename, from_path=CONFIG['DIR_TO_SCAN'], to_path=CONFIG['DESTINATION_DIR']):
    # 切换文件状态，防止再被检查
    update_file_with_status(filename, 1002)
    # 这行代码的作用是允许连接不在know_hosts文件中的主机。
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CONFIG['DESTINATION_HOST'],
                CONFIG['DESTINATION_HOST_PORT'],
                CONFIG['DESTINATION_HOST_USER'],
                CONFIG['DESTINATION_HOST_PASS'])
    sftp = ssh.open_sftp()
    try:
        # 发送文件
        sftp.put(from_path + filename, to_path + filename)
        update_file_with_status(filename, 2000)
    except IOError, e:
        # 保存错误至数据库
        try:
            wrong_file = session.query(File).filter(File.name == filename and File.status == 1000).one()
            wrong_file.status = 1001
            session.add(wrong_file)
            session.commit()
        except NoResultFound:
            logger.error('fatal error: try to transmit an unsaved file!')
        finally:
            session.close()
        # 重试
        raise IOError('[Trans]:IOError detected, please check your file path!')
    finally:
        sftp.close()
        ssh.close()
