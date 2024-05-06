from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_msearch import Search


class Profile(db.Model):
    ''' Model class '''
    __tablename__ = "userdetails"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_photo = db.Column(db.String(30), unique=True, nullable=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    designation = db.Column(db.String(30), unique=False, nullable=False)
    contact_no = db.Column(db.BIGINT, unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(1000), unique=False, nullable=False)
    course = relationship("Course", back_populates='profile')
    enrollment = relationship("Enrollments", back_populates='profile')


class Course(db.Model):
    '''Courses Model'''
    __tablename__ = "course"
    __searchable__=['name','description','start_date','end_date']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    start_date = db.Column(db.Date, unique=False, nullable=False)
    end_date = db.Column(db.Date, unique=False, nullable=False)
    link = db.Column(db.String(1000), unique=False, nullable=False)
    teacher_id = db.Column(db.Integer, ForeignKey('userdetails.id'))
    profile = relationship("Profile", back_populates='course')
    enrollment = relationship("Enrollments", back_populates='course')


class Enrollments(db.Model):
    '''Courses Model'''
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, ForeignKey('course.id'))
    sid = db.Column(db.Integer, ForeignKey('userdetails.id'))
    enroll_date = db.Column(db.Date, unique=False, nullable=False)
    cancelled = db.Column(db.Boolean, unique=False,
                          nullable=False, default=False)
    cancelled_reason = db.Column(db.String(500), unique=False, nullable=True)
    course = relationship("Course", back_populates='enrollment')
    profile = relationship("Profile", back_populates='enrollment')
