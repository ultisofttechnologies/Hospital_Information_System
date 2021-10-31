import os,sys,subprocess,platform
import pdfkit
from numpy import genfromtxt
import csv
from flask import send_file,make_response,flash,Blueprint,render_template, redirect,url_for,request,session,abort
from project import db,app
from flask_cors import CORS
from project import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from project.staff.models import Staff
from datetime import date,datetime,timedelta
from sqlalchemy import extract,text,func,and_,desc,asc
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user
from dotenv import load_dotenv
from itertools import filterfalse
from calendar import monthrange

medication_blueprint = Blueprint('medication',__name__,template_folder='templates/medication',static_folder='static',static_url_path='/static/')

@medication_blueprint.route('/new_medication',methods = ['GET','POST'])
#@login_required
def newMedication ():
  title = 'Natural Solutions Herbal Clinic | New Medication'
  messages = ''
  messages = 'New Medication messages to popup'
  return render_template('newMedication.html',title=title, messages=messages)


@medication_blueprint.route('/completed_medications',methods = ['GET','POST'])
#@login_required
def completedMedications ():
  title = 'Natural Solutions Herbal Clinic | Completed Medications'
  messages = ''
  messages = 'Completed Medications messages to popup'
  return render_template('completedMedications.html',title=title, messages=messages)

@medication_blueprint.route('/requested_medications',methods = ['GET','POST'])
#@login_required
def requestedMedications ():
  title = 'Natural Solutions Herbal Clinic | Requested Medications'
  messages = ''
  messages = 'Requested Medications messages to popup'
  return render_template('requestedMedications.html',title=title, messages=messages)

@medication_blueprint.route('/edit/<id>',methods = ['GET','POST'])
#@login_required
def editMedication (id):
  title = 'Natural Solutions Herbal Clinic | Edit Medication'
  messages = ''
  messages = 'Edit Medications messages to popup'
  return render_template('editMedication.html',title=title, id=id, messages=messages)

@medication_blueprint.route('/delete/<id>',methods = ['GET','POST'])
#@login_required
def deleteMedication (id):
  title = 'Natural Solutions Herbal Clinic | Delete Medication'
  messages = ''
  messages = 'Delete Medication messages to popup'
  return render_template('deleteMedication.html',title=title, id=id, messages=messages)
