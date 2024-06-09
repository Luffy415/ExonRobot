"""
MIT License

Copyright (c) 2022 ABISHNOI69

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1m
#     UPDATE   :- Abishnoi_bots
#     GITHUB :- ABISHNOI69 ""


import threading

from sqlalchemy import Boolean, Column, String

from Zen.modules.sql import BASE, SESSION


class CleanLinked(BASE):
    __tablename__ = "clean_linked"
    chat_id = Column(String(14), primary_key=True)
    status = Column(Boolean, default=False)

    def __init__(self, chat_id, status):
        self.chat_id = str(chat_id)
        self.status = status


CleanLinked.__table__.create(checkfirst=True)

CLEANLINKED_LOCK = threading.RLock()


def getCleanLinked(chat_id):
    try:
        if resultObj := SESSION.query(CleanLinked).get(str(chat_id)):
            return resultObj.status
        return False  # default
    finally:
        SESSION.close()


def setCleanLinked(chat_id, status):
    with CLEANLINKED_LOCK:
        if prevObj := SESSION.query(CleanLinked).get(str(chat_id)):
            SESSION.delete(prevObj)
        newObj = CleanLinked(str(chat_id), status)
        SESSION.add(newObj)
        SESSION.commit()
