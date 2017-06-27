# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
# engine = create_engine('mysql+pymysql://lsm1993:123456@192.168.2.201:3306/test')
engine = create_engine('mysql+pymysql://lsm1993:123456@127.0.0.1:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
