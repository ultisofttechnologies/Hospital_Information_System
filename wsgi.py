from project import app,db
from flask import render_template
from flask import request, jsonify
#import jsonpickle
#from project.manager.models import User,Order,Payment,Stockcountpayment,Product
from flask_login import login_user,login_required
#from sqlalchemy import extract,text,func,and_,desc,asc
#from datetime import date,datetime,timedelta
#from dateutil.relativedelta import relativedelta
#from functools import wraps


@app.route('/')
@login_required
def index ():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
