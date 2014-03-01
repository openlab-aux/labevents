from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g

from labevents import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

@app.before_request
def initialize_database_session():
    g.db = Session()
    
@app.after_request
def teardown_database_session(response):
    g.db.close()
    g.db = None
    
    return response
    
