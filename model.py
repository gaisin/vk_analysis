from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine("sqlite:///groups.db")
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

Base = declarative_base()

class Group(Base):
	__tablename__ = 'group'
	group_id = Column('group_id', Integer(), primary_key=True)

class Post_data(Base):
	__tablename__ = 'post_data'
	group_id = Column('group_id', Integer(), ForeignKey('group.group_id'))
	post_id = Column('post_id', String(100), primary_key=True)
	post_text = Column('post_text', String(300), nullable=False)

class Comment_data(Base):
	__tablename__ = 'comment_data'
	id = Column('id', Integer(), primary_key=True, autoincrement=True)
	post_id = Column('post_id', String(100), ForeignKey('post_data.post_id'))
	comment_id = Column('comment_id', Integer(), nullable=False)
	comment_text = Column('comment_text', Text(), nullable=False)
	likes = Column('likes', Integer(), nullable=False)


