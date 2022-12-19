from sqlalchemy import Column, Boolean, Integer, String, SmallInteger, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship("Student", backref=backref("user", uselist=False))


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    students = relationship('Student', back_populates='group')
    subjects = relationship("Subject", secondary="groups_subjects", back_populates="groups")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(SmallInteger)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', back_populates='students')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name_of_subject = Column(String(50))
    groups = relationship("Group", secondary="groups_subjects", back_populates="subjects")


class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    date_time = Column(DateTime)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))


class Rating(Base):
    __tablename__ = 'ratings'
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
    value = Column(SmallInteger)


groups_subjects = Table('groups_subjects', Base.metadata,
                        Column('group_id', ForeignKey('groups.id'), primary_key=True),
                        Column('subject_id', ForeignKey('subjects.id'), primary_key=True)
                        )
