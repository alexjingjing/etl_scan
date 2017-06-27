# -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_

from app.model.file import File
from app.util import session


def get_file_to_trans():
    try:
        result = session.query(File).filter(File.status == 1001).all()
    except NoResultFound:
        result = []
    return result


def update_file_with_status(filename, status):
    session.query(File).filter(File.name == filename).update({File.status: status})
    session.commit()
