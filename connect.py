from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "sqlite:///db.sqlite"
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
