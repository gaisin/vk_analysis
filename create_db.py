import os
basedir = os.path.abspath(os.path.dirname(__file__))

from sqlalchemy import create_engine
engine = create_engine('sqlite:///' + os.path.join(basedir, '..', 'groups.db'), echo=True)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
metadata = MetaData()

group = Table('group', metadata,
	Column('group_id', Integer(), primary_key=True)
)
post_data = Table('post_data', metadata,
	Column('group_id', Integer(), ForeignKey('group.group_id')),
	Column('post_id', String(100), primary_key=True),
	Column('post_text', String(300), nullable=False)
)
comment_data = Table('comment_data', metadata,
	Column('id', Integer(), primary_key=True, autoincrement=True),
	Column('post_id', String(100), ForeignKey('post_data.post_id')),
	Column('comment_id', Integer(), nullable=False),
	Column('comment_text', Text(), nullable=False),
	Column('likes', Integer(), nullable=False)
)

metadata.create_all(engine)