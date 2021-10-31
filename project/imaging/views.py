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

imaging_blueprint = Blueprint('imaging',__name__,template_folder='templates/imaging',static_folder='static',static_url_path='/static/')

@imaging_blueprint.route('/new_imaging',methods = ['GET','POST'])
#@login_required
def newImaging ():
  title = 'Natural Solutions Herbal Clinic | New Imaging'
  return render_template('newImaging.html',title=title)


@imaging_blueprint.route('/view_imaging',methods = ['GET','POST'])
#@login_required
def viewImaging ():
  title = 'Natural Solutions Herbal Clinic | View Imaging'
  return render_template('viewImaging.html',title=title)
