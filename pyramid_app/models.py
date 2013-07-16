from sqlalchemy import Column, Integer, Float, Text, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from datetime import datetime
from time import strftime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    group = Column(Text, nullable=False)

class UserSearch(Base):

    __tablename__ = 'search'
    search_id = Column(Integer, primary_key=True)
    _last_update = Column(DateTime, default=datetime.today, onupdate=datetime.today)
    search_content = Column(Text, primary_key=True, nullable=False)
    all_link = Column(Text, nullable=False)
    all_price = Column(Float, nullable=False)
    nok_link = Column(Text, nullable=False)
    nok_price = Column(Float, nullable=False)
    search_quantity = Column(Integer, nullable=False)


    @property
    def last_update(self):
        return self._last_update.strftime("%Y-%m-%d %H:%M:%S")