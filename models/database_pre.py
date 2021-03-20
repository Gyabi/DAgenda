from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# データベースの基本設定
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "agenda.db")
engin = create_engine("sqlite:///" + database_file, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engin))
Base = declarative_base()
Base.query = db_session.query_property()


# この関数を実行するとdbを初期化できる
def init_db():
    import models.models
    Base.metadata.create_all(bind=engin)