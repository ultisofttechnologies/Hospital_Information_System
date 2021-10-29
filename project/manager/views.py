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


manager_blueprint = Blueprint('manager',__name__,template_folder='templates/manager',static_folder='static',static_url_path='/static/')
@manager_blueprint.route('/login',methods = ['GET','POST'])
#@login_required
def login ():
    db.create_all()
    title = 'Natural Solutions Herbal Clinic | Login'
    if request.method == 'POST':
        if request.form['submit'] == 'Login':
            user_name = request.form['username']
            user_name = user_name.strip()
            password = request.form['password']
            user = Staff.query.filter(Staff.username==user_name).first()
            if user==None:
                flash('Please enter user name correctly')
            else:
                if user.check_password(password) and user!= None:
                    login_user(user)
                    next = request.args.get('next')
                    if next==None or next[0]!='/':
                        next = url_for('index')
                    return redirect(next)
                else:
                    flash('Please enter correct login credentials')
        else:
            pass
    return render_template('login.html',title=title)

@manager_blueprint.route('/add_user',methods = ['GET','POST'])
#@login_required
def addUser ():
    db.create_all()
    title = 'Natural Solutions Herbal Clinic | Login'
    staff_positions = ['Manager','Employee']
    if request.method == 'POST':
        if request.form['submit'] == 'Register':
            name = request.form['full_name']
            name = name.strip().title()
            password = request.form['password']
            password_confirm = request.form['password_confirm']
            user_name = request.form['user_name']
            user_name= user_name.strip()
            registration_code = request.form['registration_code']
            privilege_column = request.form['select_privilege']
            contact = request.form['contact']
            date_of_birth = request.form['dateofbirth']
            staff_id_number = request.form['staff_id_number']
            sex = request.form['sex']
            qualification = request.form['qualification']
            emergency_contact = request.form['emergency_contact']
            date_of_start = request.form['date_of_start']
            position = request.form['position']
            relationship_to_emergency_contact = request.form['relationship_to_emergency_contact']
            check = generate_password_hash(password)
            if check_password_hash(check,password_confirm) and registration_code =='pbkdf2:sha256:150000$qlK8X5Zr$7a90d78e7d61b4ccb9b57bdc2e3a7af1027b56e7b6eb1d55a26b8b38af69f907':
                if Staff.query.filter(Staff.username==user_name).first()==None:
                    if privilege_column == 'Manager':
                        new_user = Staff(user_name,password,0)
                        new_user.name = name
                        new_user.date_of_birth = date_of_birth
                        new_user.staff_id_number = staff_id_number
                        new_user.contact = contact
                        new_user.position = position
                        new_user.qualification = qualification
                        new_user.relationship_to_emergency_contact = relationship_to_emergency_contact
                        new_user.date_of_start = date_of_start
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for('manager.login'))
                    elif privilege_column == 'Employee':
                        new_user = Staff(user_name,password,1)
                        new_user.name = name
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for('manager.login'))
                    else:
                        flash('Please select a privilege level')
                else:
                    flash('Username already taken, please enter a new one')
            else:
                flash('Password mismatch, or wrong registration code entered!')
        else:
            pass
    return render_template('addUser.html',title=title,staff_positions=staff_positions)
