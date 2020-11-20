from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:$ssmi119$@localhost:3306/api1'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_STRING')
db = SQLAlchemy(app)
