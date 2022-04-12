from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column('id', Integer, primary_key=True)
    discordid = Column('discordId', String, unique=True)
    username = Column('username', String, unique=True)
    lastDaily = Column('lastdaily', DateTime)

    def __repr__(self):
        return '<User discordid:%d - username:%s - lastDaily: %s' % (discordid, username, lastDaily)


class Item(Base):
    __tablename__ = "objet"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    


engine = create_engine('sqlite:///:memory:', echo=True, future=True)
Base.metadata.create_all(bind=engine)