from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from models.database import Base
from datetime import datetime


# データベースのカラムを設定
class ProjectContent(Base):
    __tablename__ = "projectcontent"
    id = Column(Integer, primary_key=True)
    project= Column(String(128), unique=True)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, project=None, date=None):
        self.project = project
        self.date =date
    
    def __repr__(self):
        return "<Project %r>" % (self.project)

class AgendaContent(Base):
    __tablename__ = "agendacontent"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    agenda = Column(String(128), unique=True)
    done = Column(Boolean)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, project_id=None, agenda=None, done=None, date=None):
        self.project_id = project_id
        self.agenda = agenda
        self.done = done
        self.date = date

    def __repr__(self):
        return "<Agenda %r>" % (self.agenda)

class CommentContent(Base):
    __tablename__ = "commentcontent"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    agenda_id = Column(Integer)
    comment = Column(Text)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, project_id=None, agenda_id=None, comment=None, date=None):
        self.project_id = project_id
        self.agenda_id = agenda_id
        self.comment = comment
        self.date = date
    
    def __repr__(self):
        return "<Comment %r>" % (self.comment)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return "<Name %r>" % (self.user_name)



