from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '3334082287403141'

if not os.path.exists('instance'):
    os.makedirs('instance')
caminho_completo = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/comunidadedb.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_completo}'

database= SQLAlchemy(app)
bcrypt= Bcrypt(app)
logim_manege= LoginManager(app)
logim_manege.login_view= 'cad_login'
logim_manege.login_message= 'Para continuar é necessario fazer login'
logim_manege.login_message_category= 'alert-info'
from comunidadeimpressionadora import routes