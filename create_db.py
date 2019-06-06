# ORM or Object Relational Mapping is essentially a way
# to use objects in our language, to represent tables
# in our DB. Along with that, they provide access to 
# DB operations without the need to get into raw SQL 
# queries.
#
# For the course that inspired this, we use SQLAlchemy.
# For those new to it, please see their tutorial below:
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# In SQLAlchemy classes are mapped using their 'declarative
# system.' We create that base class here.
Base = declarative_base()

# We then define our class which will inherit from our
# declarative base created above.
# NOTE: You can declare multiple tables to inherit from
# your Base object, in this example we just have one.
class Todo(Base):
    # Here you declare what your table name will be
    __tablename__ = 'todo'

    # These specify what columns your table will have.
    # The names, id/name/isCompleted become the name
    # of the column in the DB
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    isCompleted = Column(Boolean, nullable = False)

# In SQLAlchemy the 'Engine' class, '... represents
# the core interface to the database,...' Since we're
# using SQLite3, we specify the DB when creating
# our engine
engine = create_engine('sqlite:///todos.db')

# Up until now we've created the table 'meta data,' nothing
# has been written to the DB. In SQLAlchemy the type
# MetaData, can be used to issue a 'CREATE TABLE' statement, 
# based on the 'todo' table we created above. For that
# we use the instance our Base class has, 'Base.metadata'
# and call its function 'create_all' passing our engine.
# At this point our DB (todos.db) now has our table(s). 
Base.metadata.create_all(engine)