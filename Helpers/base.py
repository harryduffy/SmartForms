from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn_str = 'mysql://admin:adminadmin@ipw.cuvxj8ktqbkz.ap-southeast-2.rds.amazonaws.com/sys'
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)

Base = declarative_base()