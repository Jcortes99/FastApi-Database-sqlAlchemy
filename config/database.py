import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "database.sqlite"

base_dir = os.path.dirname(os.path.realpath(__file__))

databse_url = f"squlite:///{os.path.join(base_dir,sqlite_file_name)}"

engine = create_engine(databse_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()