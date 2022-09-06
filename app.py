from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy import exc
import os
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship
from flask_cors import CORS
db_path = os.path.join(os.path.dirname(__file__), 'network.db')
db_uri = 'sqlite:///{}'.format(db_path)


app = Flask(__name__)
CORS(app, origins=['*', 'localhost:5173'])


app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from cmd import *
from user import *
from device import *
from script import *
from group import *
from office import *
from enable_ssh_disable_telnet import *
from scan import *
from wilaya import *

