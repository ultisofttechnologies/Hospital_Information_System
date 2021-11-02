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

laboratory_blueprint = Blueprint('laboratory',__name__,template_folder='templates/laboratory',static_folder='static',static_url_path='/static/')

@laboratory_blueprint.route('/new_lab',methods = ['GET','POST'])
#@login_required
def newLabs ():
  title = 'Natural Solutions Herbal Clinic | New Laboratory'
  messages = ''
  messages = 'New Laboratory messages to popup'
  return render_template('newLab.html',title=title, messages=messages)

@laboratory_blueprint.route('/requested_labs',methods = ['GET','POST'])
#@login_required
def requestedLabs ():
  title = 'Natural Solutions Herbal Clinic | Requested Laboratorys'
  messages = ''
  messages = 'Requested Laboratorys messages to popup'
  return render_template('requestedLabs.html',title=title, messages=messages)

@laboratory_blueprint.route('/completed_labs',methods = ['GET','POST'])
#@login_required
def completedLabs ():
  title = 'Natural Solutions Herbal Clinic | Completed Laboratorys'
  messages = ''
  messages = 'Completed Laboratorys messages to popup'
  return render_template('completedLabs.html',title=title, messages=messages)

@laboratory_blueprint.route('/edit/<id>',methods = ['GET','POST'])
#@login_required
def editLab (id):
  title = 'Natural Solutions Herbal Clinic | Edit Lab'
  messages = ''
  messages = 'Edit Lab messages to popup'
  return render_template('editLab.html',title=title, id=id, messages=messages)

@laboratory_blueprint.route('/delete/<id>',methods = ['GET','POST'])
#@login_required
def deleteLab (id):
  title = 'Natural Solutions Herbal Clinic | Delete Lab'
  messages = ''
  messages = 'Delete Lab messages to popup'
  return render_template('deleteLab.html',title=title, id=id, messages=messages)

