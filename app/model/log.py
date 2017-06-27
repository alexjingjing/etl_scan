# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, BIGINT, TIMESTAMP

from app.model import Base


class Log(Base):
    # 表名
    __tablename__ = 'log'

    # 表结构
    id = Column(BIGINT, primary_key=True)
    message = Column(String(100))
    task_id = Column(String(50))
    update_time = Column(TIMESTAMP)
