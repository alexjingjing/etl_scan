# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, String, BIGINT, INTEGER, DATETIME

from app.model import Base


class File(Base):
    # 表名
    __tablename__ = 'file'

    # 表结构
    id = Column(BIGINT, primary_key=True)
    name = Column(String(100))
    status = Column(INTEGER)
    date = Column(String())
    update_time = Column(DATETIME, default=datetime.datetime.now)
    extract_file_names = Column(String(200))

    def __init__(self, name, status, date):
        self.name = name
        self.status = status
        self.date = date

    def __repr__(self):
        return 'file name is %s' % self.name
