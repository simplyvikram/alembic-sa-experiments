
import logging
import os
import sys


from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DevelopmentConfig
from config import ProductionConfig

# we want the mapping between Models and tables to be instumented
from application.models import *
from application.models_tables import *

app = Flask(__name__)

# set up config
if 'APP_ENV' in os.environ and os.environ['APP_ENV'] == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# set up db connection
engine = create_engine(app.config['DATABASE_URI'])
session = sessionmaker(engine)()
# session = Session()


# setting logging
handler = logging.StreamHandler(sys.stdout)
formatter = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
