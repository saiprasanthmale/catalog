import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)


class College_Name(Base):
    __tablename__ = 'college_name'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="bank_name")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class Student_Details(Base):
    __tablename__ = 'student_details'
    id = Column(Integer, primary_key=True)
    stu_name = Column(String, nullable=False)
    stu_rnumber = Column(String(150))
    stu_phone_number = Column(Integer)
    stu_course = Column(String, nullable=False)
    stu_address = Column(String(150), nullable=False)
    slink = Column(String(350))
    college_name_id = Column(Integer, ForeignKey('college_name.id'))
    college_name = relationship(
        College_Name, backref=backref(
            'student_details', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="student_details")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'stu_name': self. stu_name,
            'stu_rnumber': self. stu_rnumber,
            'stu_phone_number': self. stu_phone_number,
            'stu_course': self. stu_course,
            'stu_address': self. stu_address,
            'slink': self. slink,
            'id': self. id
        }

eng = create_engine('sqlite:///college_db.db')
Base.metadata.create_all(eng)
