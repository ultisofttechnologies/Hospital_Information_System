import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_cors import CORS
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask (__name__,static_folder='static',static_url_path='/static/')
# CORS(app)

ALLOWED_EXTENSIONS = {'csv'}
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='secretkey'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD']=True
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)
Migrate(app,db)
login_manager.init_app(app)
login_manager.login_view = 'manager.login'
#
from project.manager.views import manager_blueprint
from project.patient.views import patient_blueprint
from project.staff.views import staff_blueprint
from project.appointment.views import appointment_blueprint
from project.medication.views import medication_blueprint
from project.imaging.views import imaging_blueprint
from project.laboratory.views import laboratory_blueprint
from project.accounts.views import accounts_blueprint
from project.inventory.views import inventory_blueprint

app.register_blueprint (manager_blueprint,url_prefix='/manager')
app.register_blueprint (patient_blueprint,url_prefix='/patient')
app.register_blueprint (staff_blueprint,url_prefix='/staff')
app.register_blueprint (appointment_blueprint,url_prefix='/appointment')
app.register_blueprint (medication_blueprint,url_prefix='/medication')
app.register_blueprint (imaging_blueprint,url_prefix='/imaging')
app.register_blueprint (laboratory_blueprint,url_prefix='/laboratory')
app.register_blueprint (accounts_blueprint,url_prefix='/accounts')
app.register_blueprint (inventory_blueprint,url_prefix='/inventory')