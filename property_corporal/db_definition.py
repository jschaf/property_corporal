__author__ = 'joe'
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EndItem(Base):
    """A representation of one item on a property book.
    """
    __tablename__ = 'enditem'
    nsn = Column(String)
    serial_number = Column(String)
