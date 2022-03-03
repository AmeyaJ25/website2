#from crypt import methods
import pickle
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from flask import *
import random
import calendar
from flask_sqlalchemy import SQLAlchemy
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY'] = 'the random string'  
db = SQLAlchemy(app)
#only for temporary hosting
# run_with_ngrok(app) 
s=URLSafeTimedSerializer("secretagain")

admin_email="dao.insurance.agency@gmail.com"
password="Dao@1234"

# Database connection and tables


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(1000),  nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    passwd = db.Column(db.String(120), nullable=False)
    Gender = db.Column(db.String(1), nullable=False)
    dob=db.Column(db.String(10),nullable=False)
    age = db.Column(db.Integer)
    #marriedstatus=db.Column(db.Integer, nullable=False)
    pastnoofclaim= db.Column(db.Integer)        

class Policy(db.Model):
    no = db.Column(db.Integer, primary_key=True,autoincrement=True)
    carno=db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    #Remove Date#Update Policy
    #date=db.Column(db.String(10), nullable=False)
    #tclaim=db.Column(db.Integer, nullable=False)
    vcat=db.Column(db.String(20), nullable=False)
    vprice=db.Column(db.String(20), nullable=False)
    agtype=db.Column(db.String(20), nullable=False)
    deduct=db.Column(db.Integer, nullable=False)
    bpolicy=db.Column(db.String(20), nullable=False)
    vage=db.Column(db.String(20), nullable=False)
    make=db.Column(db.String(20), nullable=False)
    ptype=db.Column(db.String(20), nullable=False)

class Claim(db.Model):
    carno1 = db.Column(db.String(12),primary_key=True, nullable=False)
    email=db.Column(db.String(120), nullable=False)
    dateacc=db.Column(db.String(15), nullable=False)
    # gender=db.Column(db.String(15), nullable=False)
    area=db.Column(db.String(15), nullable=False)
    marriedstatus=db.Column(db.String(15), nullable=False)
    reportfiled=db.Column(db.String(15), nullable=False)
    witnesspresent=db.Column(db.String(15), nullable=False)
    fault=db.Column(db.String(15), nullable=False)
    noofcars=db.Column(db.String(20), nullable=False)
    dpa=db.Column(db.String(20), nullable=False)
    dpc=db.Column(db.String(20), nullable=False)
    prediction=db.Column(db.String(10),nullable=False)
    #Days_Policy_Accident={'none':0, '1 to 7':4, '8 to 15':11.5, '15 to 30':22.5,'more than 30':31}
    #Days_Policy_Claim={'8 to 15':11.5, '15 to 30':22.5,'more than 30':31}

#Dictionary
Make={'Honda':0, 'Toyota':1, 'Ford':2, 'Mazda':3, 'Chevrolet':4, 'Pontiac':5,
       'Accura':6, 'Dodge':7, 'Mercury':8, 'Jaguar':9, 'Nisson':10, 'VW':11, 'Saab':12,
       'Saturn':13, 'Porche':14, 'BMW':15, 'Mecedes':16, 'Ferrari':17, 'Lexus':18}


MaritalStatus={'Single':0, 'Married':1, 'Widow':2, 'Divorced':3}


PolicyType={'Sport - Liability':0, 'Sport - Collision':1, 'Sedan - Liability':2,
       'Utility - All Perils':3, 'Sedan - All Perils':4, 'Sedan - Collision':5,
       'Utility - Collision':6, 'Utility - Liability':7, 'Sport - All Perils':8}

VehicleCategory={'Sport':0, 'Utility':1, 'Sedan':2}

BasePolicy={'Liability':0, 'Collision':1, 'All Perils':2}

Month={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
DayOfWeek={'Monday':1, 'Tuesday':2,'Wednesday':3,'Thursday':4, 'Friday':5, 'Saturday':6,'Sunday':7}
AccidentArea={'Urban':1, 'Rural':0}
DayOfWeekClaimed={'Monday':1, 'Tuesday':2,'Wednesday':3,'Thursday':4, 'Friday':5, 'Saturday':6,'Sunday':7}
MonthClaimed={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
VehiclePrice={'less than 20000':19999,'20000 to 29000':24500, '30000 to 39000':34500,'40000 to 59000':49500,
              '60000 to 69000':64500,'more than 69000':69001}
Days_Policy_Accident={'none':0, '1 to 7':4, '8 to 15':11.5, '15 to 30':22.5,'more than 30':31}
Days_Policy_Claim={'8 to 15':11.5, '15 to 30':22.5,'more than 30':31}
PastNumberOfClaims={'none':0, '1':1, '2 to 4':2, 'more than 4':5}
AgeOfVehicle={ 'new':0,'2 years':2 ,'3 years':3,'4 years':4 ,'5 years':5 , '6 years':6, '7 years':7,
              'more than 7':8}
# AgeOfPolicyHolder={'16 to 17':,'18 to 20':,'21 to 25':,'26 to 30':, '31 to 35':,'36 to 40':,
#                    '41 to 50':, '51 to 65':,'over 65':}
NumberOfSuppliments={'none':0,'1 to 2':1,'3 to 5':3,'more than 5':6}
AddressChange_Claim={'no change':0,'under 6 months':0.5,'1 year':1,'2 to 3 years':2.5,'4 to 8 years':6}
NumberOfCars={'1 vehicle':1, '2 vehicles':2,'3 to 4':3.5,'5 to 8':6.5, 'more than 8':9}

Gender={'Female':1, 'Male':0}
AccidentArea={'Urban':1, 'Rural':0}
MaritalStatus={'Single':0, 'Married':1, 'Widow':2, 'Divorced':3}
PoliceReportFiled={'Yes':1, 'No':0}
WitnessPresent={'Yes':1, 'No':0}
Fault={'Policy Holder':1, 'Third Party':0}
Deductible={'300', '400', '500', '700'}
AgentType={'External':1, 'Internal':0}
# home route

@app.route("/")
def home():
    return render_template("home.html")
###################################

# Login for customer

@app.route("/Cuslog", methods=['GET','POST'])
def customer_login():
    if(request.method == "POST"):
        email=request.form.get("email")
        password=request.form.get("passwd")
        q=User.query.filter_by(email=email).first()
        if(q and q.passwd==password):
            session["username"]=email
            return render_template("cussuc.html",usrname=session["username"])
        else:
            flash("*Incorrect Email or Password")
            return redirect(url_for("customer_login"))
    else:
        return render_template("customer_login.html")
############################
#Customer reset password
@app.route("/reset",methods=["POST","GET"])
def reset():
    if request.method=="POST":
        email=request.form.get("email")
        q=User.query.filter_by(email=email).first()
        if(q):
            token=s.dumps(email,salt="email-config")
            sender_question="Reset Password"
            link=url_for('confirmemail',token=token, _external=True)
            admin_ans="To reset your Password open this link {}".format(link)
            useremail=q.email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "RESET your Password"
            msg['From'] = admin_email
            msg['To'] = useremail
            html=render_template("reset_mail.html",sender_question=sender_question,admin_ans=admin_ans)
            message="Reply from DAO Insurance"
            part1 = MIMEText(message, 'plain')
            part2 = MIMEText(html, 'html')  
            msg.attach(part1)
            msg.attach(part2)
            server=smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("dao.insurance.agency@gmail.com","Dao@1234")
            server.sendmail(admin_email,useremail,msg.as_string())
            flash("To reset your password check your Registered email")
            return redirect(url_for("customer_login"))
        else:
            flash("No such email id registered")
            return render_template("customer_login.html")
########################
#confirm token
@app.route("/confirm/<token>")
def confirmemail(token):
    try:
        email=s.loads(token,salt='email-config',max_age=600)
        return redirect(url_for('resetpassword',email=email))
    except SignatureExpired:
        return '<h1 The token is expired ! </h1'

####################
#reset password

@app.route("/addpassword/<email>",methods=["GET","POST"])
def resetpassword(email):
    if request.method=="POST":
        password=request.form.get("password")
        q=User.query.filter_by(email=email).first()
        q.passwd=password
        db.session.add(q)
        db.session.commit()
        flash("Password reseted successfully")
        return redirect(url_for("customer_login"))
    else:
        return render_template("reset.html")

        
# Route for admin login

@app.route("/adlog", methods=['GET','POST'])
def admin_login():
    if(request.method=='POST'):
        email=request.form.get("email")
        password=request.form.get("pass")
        if(email== "ADMIN" and password == "a"):
            session["admin"] = email
            return redirect(url_for("admin_home"))
        else:
            flash("*Incorrect Email or Password")
            return redirect(url_for("admin_login"))
    return render_template("admin_login.html")
###########################

#Route to show all users registered
@app.route("/usersdisp", methods=['GET','POST'])
def userdisp():
    if not session.get("admin"):
      return render_template("illegal.html")  
    data23=User.query.all()
    return render_template("userdisp.html",usr=data23)


# Route for contact form and add data to db


@app.route("/contact", methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        name=request.form.get("name")
        email=request.form.get("email")
        msg=request.form.get("msg")
        query=Contact(name=name,email=email,msg=msg)
        db.session.add(query)
        db.session.commit()
        flash("Your message is send to admin panel you will be notified soon")
        return redirect(url_for("home"))
    else:
        return render_template("contact.html")
################################

# display message send from contact form

@app.route("/notcontact")
def fetch_contact():
    if not session.get("admin"):
      return render_template("illegal.html")  
    data=Contact.query.all()
    return render_template("viewdata.html",data=data)
########################


# Logout session for admin and User

@app.route("/logout/<sess>")
def logout(sess):
    if sess=="ADMIN":
        new="admin"
        session.pop(new , None)
    else:
        new="username"
        session.pop(new, None)
    return redirect(url_for('home'))
#####################

# Add new user from admin
@app.route("/adduser",methods=["GET","POST"])
def adduserdb():
    if not session.get("admin"):
      return render_template("illegal.html") 
    today=date.today()
    today2=today-relativedelta(years=18)
    today2=str(today2)
    return render_template("add_user.html",today2=today2)

@app.route("/adduserdb",methods=["GET","POST"])
def adduser():
    if not session.get("admin"):
      return render_template("illegal.html")
    elif(request.method=='POST'):
        name=request.form.get("name")
        email=request.form.get("email")
        passwd=request.form.get("passwd")
        gender=request.form.get("gender")
        date=request.form.get("DOB")
        datetime_object = datetime.strptime(date, '%Y-%m-%d')
        today1 = datetime.today()
        age = today1.year - datetime_object.year -((today1.month, today1.day) <
         (datetime_object.month, datetime_object.day))
        q=User(name=name,email=email,passwd=passwd,Gender=gender,dob=date,age=age,pastnoofclaim=0)
        db.session.add(q)
        db.session.commit()
        flash("New user added successfully")
        sender_question="Your Login credentials are:"
        admin_ans="Username:- {} \n Password:- {} ".format(email,passwd)
        useremail=q.email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Your Account on DAO"
        msg['From'] = admin_email
        msg['To'] = email
        html=render_template("mail.html",sender_question=sender_question,admin_ans=admin_ans)
        message="Reply from DAO Insurance"
        part1 = MIMEText(message, 'plain')
        part2 = MIMEText(html, 'html')  
        msg.attach(part1)
        msg.attach(part2)
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("dao.insurance.agency@gmail.com","Dao@1234")
        server.sendmail(admin_email,useremail,msg.as_string())
        return redirect(url_for("admin_home"))
    else:
        if not session.get("admin"):
            return render_template("illegal.html")
        return render_template("add_user.html")
#################################

# send mail for contact form message given by admin

@app.route("/sendmail/<useremail>",methods=["GET","POST"])
def sendmailad(useremail):
    if request.method=="POST":
        q=Contact.query.filter_by(email=useremail).first()
        sender_question=q.msg
        admin_ans=request.form.get("admin_reply")
        useremail=q.email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Message from DAO Insurance"
        msg['From'] = admin_email
        msg['To'] = useremail
        html=render_template("mail.html",sender_question=sender_question,admin_ans=admin_ans)
        message="Reply from DAO Insurance"
        part1 = MIMEText(message, 'plain')
        part2 = MIMEText(html, 'html')  
        msg.attach(part1)
        msg.attach(part2)
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("dao.insurance.agency@gmail.com","Dao@1234")
        server.sendmail(admin_email,useremail,msg.as_string())
        db.session.delete(q)
        db.session.commit()
        return redirect(url_for("admin_home"))
    else:
        render_template_string("illegal.html")
############################

# admin home page
@app.route("/adsuc")
def admin_home():
    if not session.get("admin"):
      return render_template("illegal.html") 
    q=User.query.all()
    userno=len(q)
    q=Contact.query.all()
    notification=len(q)
    q=Policy.query.all()
    policyno=len(q)
    q=Claim.query.all()
    claimno=len(q)
    return render_template("adsuc.html",userno=userno,notification=notification,policyno=policyno,claimno=claimno)
##########################

#delete User

@app.route("/delete",methods=['GET','POST'])
def remove():
    if request.method=='POST':
        email=request.form.get("email")
        q=User.query.filter_by(email=email).first()
        db.session.delete(q)
        db.session.commit()
        flash("User deleted successfully")
        return redirect(url_for("admin_home"))
    else:
        return redirect(url_for("admin_home"))
###########################
#admin claim page
@app.route("/claim")
def adclaim():
    if not session.get("admin"):
      return render_template("illegal.html") 
    q2=Claim.query.all()
    q3=User.query.all()
    return render_template("adclaim.html",v2=q2,v3=q3)
###########################
#update policy
@app.route("/update",methods=['GET','POST'])
def updatepol():
    if not session.get("admin"):
      return render_template("illegal.html") 
    elif request.method=="POST":
        carno=request.form["carno"]
        email=request.form["email"]
        #date=request.form["date"]
        #tclaim=request.form["claim"]
        ###
        vehiclecategory=request.form["vehiclecat"]
        basepolicy=request.form["basepolicy"]
        agevehicle=request.form["agevehicle"]
        company=request.form["company"]
        vehicleprice=request.form["vehicleprice"]
        Deductable=request.form["deductable"]
        agenttype=request.form["agenttype"]
        policytype=request.form["policytype"]
        q=Policy(carno=carno,email=email,vcat=vehiclecategory,vprice=vehicleprice,agtype=agenttype,deduct=Deductable,bpolicy=basepolicy,vage=agevehicle,make=company,ptype=policytype)
        db.session.add(q)
        db.session.commit()
        flash("Policy updated")
        return redirect(url_for("admin_home"))
    else:
        return render_template("updatepol.html")
####################
#route for customer homepage

@app.route("/cussuc")
def cussuccess():
    if not session.get("username"):
      return render_template("illegal.html") 
    return render_template("cussuc.html")
#route for apply claim
@app.route("/applyclaim")
def aclaim():
    if not session.get("username"):
      return render_template("illegal.html") 
    today=date.today()
    today1=str(today)
    return render_template("appclaim.html",today1=today1)

#route for add claim
@app.route("/addclaim",methods=['GET','POST'])
def addclaim():
    # if (request.method=='POST'):
    #     email1=session["username"]
    #     dateacc1=request.form.get("DOA")
    #     gender1=request.form.get("gender1")
    #     carno2=request.form.get("carno1")
    #     area=request.form.get("Area")
    #     mstatus=request.form.get("Status")
    #     repofiled=request.form.get("PoliceR")
    #     witness1=request.form.get("witness")
    #     fault1=request.form.get("fault")
    #     nofcars=request.form.get("CarsInvolved")
    #     daypacc=request.form.get("daypolicyacc")
    #     daypcla=request.form.get("daypolicycla")
    #     q3=User.query.filter_by(email=email1).first()
    #     n=q3.pastnoofclaim
    #     n=n+1
    #     q3.pastnoofclaim=n
    #     db.session.add(q3)
    #     db.session.commit()
        
    #     # datetime_object = datetime.strptime(date, '%Y-%m-%d')
    #     # today1 = datetime.today()
    #     # age = today1.year - datetime_object.year -((today1.month, today1.day) <
    #     #  (datetime_object.month, datetime_object.day))
    #     q1=Claim(email=email1,dateacc=dateacc1,gender=gender1,area=area,marriedstatus=mstatus,reportfiled=repofiled,witnesspresent=witness1,fault=fault1,noofcars=nofcars,dpa=daypacc,dpc=daypcla,carno1=carno2)
    #     db.session.add(q1)
    #     db.session.commit()
    #     flash("Claim added successfully")
    #     return render_template("cussuc.html")
    # else:
    #     if not session.get(session['username']):
    #         return render_template("illegal.html")
    #     return render_template("cussuc.html")
    c=[]
    pre=[]
    if (request.method=='POST'):
        email1=email=session["username"]
        dateacc1=request.form.get("DOA")
        dateacc1=str(dateacc1)
        
        area=request.form.get("Area")
        mstatus=request.form.get("Status")
        repofiled=request.form.get("PoliceR")
        witness1=request.form.get("witness")
        fault1=request.form.get("fault")
        nofcars=request.form.get("CarsInvolved")
        vehicleno=request.form["carno1"]
        q5=Policy.query.filter_by(carno=vehicleno).first()
        if(q5):

            quser=User.query.filter_by(email=email1).first()
            q=Policy.query.filter_by(email=email1,carno=vehicleno).first()
            moddate = datetime.strptime(dateacc1, '%Y-%m-%d')
            def week_number_of_month(date_value):
                return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)
            p1=moddate.month #1
            p2=week_number_of_month(moddate)#(moddate.day)/7 #2
            p3=(moddate.weekday()) #3
            weekday2=calendar.day_name[p3]
            p3=DayOfWeek[weekday2]
            # print("---------------------------")
            #print(p2 ,weekday2 ,p3)
            make=q.make
            p4=Make[make] #4
            p5=AccidentArea[area] #5
            today=date.today()
            today=str(today)
            claimdate = datetime.strptime(today,'%Y-%m-%d')
            p6=(claimdate.weekday()) #6
            weekday3=calendar.day_name[p6]
            p6=DayOfWeek[weekday3]
            p7=(claimdate.month) #7
            p8=week_number_of_month(claimdate) #8
            #print(p6 ,weekday3 ,p8)
            gender1=quser.Gender
            p9=Gender[gender1] #9
            p10=MaritalStatus[mstatus] #10
            p11=quser.age #11
            p12=Fault[fault1] #12
            poltype=q.ptype
            p13=PolicyType[poltype] #13
            vehicat=q.vcat
            p14=VehicleCategory[vehicat] #14
            p15=q.vprice #15
            p15=VehiclePrice[p15]
            #p16 = random.randint(0,15420) #16
            p16=q.deduct #17
            p17=request.form["daypolicyacc"] #18
            dayacc=p17
            p17=Days_Policy_Accident[p17]
            p18=request.form["daypolicycla"] #19
            dayclaim=p18
            p18=Days_Policy_Claim[p18]
            p19=quser.pastnoofclaim #20
            p20=q.vage #21
            p20=AgeOfVehicle[p20]
            p21=PoliceReportFiled[repofiled] #22
            p22=WitnessPresent[witness1] #23
            agenttype=q.agtype
            p23=AgentType[agenttype] #24
            p24=NumberOfCars[nofcars] #25 
            basepolicy=q.bpolicy
            p25=BasePolicy[basepolicy] #26
            c.append(p1)
            c.append(p2)
            c.append(p3)
            c.append(p4)
            c.append(p5)
            c.append(p6)
            c.append(p7)
            c.append(p8)
            c.append(p9)
            c.append(p10)
            c.append(p11)
            c.append(p12)
            c.append(p13)
            c.append(p14)
            c.append(p15)
            #c.append(p16)
            c.append(p16)
            c.append(p17)
            c.append(p18)
            c.append(p19)
            c.append(p20)
            c.append(p21)
            c.append(p22)
            c.append(p23)
            c.append(p24)
            c.append(p25)
            # print("---------------------------")
            # for i in c:
            #     print(type(i))
            pre.append(c)
            model=pickle.load(open("Finalmodel.sav", 'rb'))#("projectXGboost.sav", 'rb'))
            op=model.predict(pre)
            if(op==[1]):
                prediction="fraud"
            else:
                prediction="genuine"
            q1=Claim(email=email1,dateacc=dateacc1,area=area,marriedstatus=mstatus,reportfiled=repofiled,witnesspresent=witness1,fault=fault1,noofcars=nofcars,dpa=dayacc,dpc=dayclaim,carno1=vehicleno,prediction=prediction)
            db.session.add(q1)
            db.session.commit()
            flash("Claim added successfully")
            return render_template("cussuc.html")
        else:
            flash("Given Car Number is not registered with your Vehicle poilcy")
            return render_template("appclaim.html")
    else:
        if not session.get(session['username']):
            return render_template("illegal.html")
        return render_template("cussuc.html")
####################
#route for admin policy view
#from datetime import datetime 
@app.route("/adpolicy")
def admin_policy():
    q=Policy.query.all()
    return render_template("adpolicy.html",data=q) 
####################
#route for customer policy view
@app.route("/viewpol")
def client_policy():
    if not session.get("username"):
      return render_template("illegal.html") 
    email=session["username"]
    q=Policy.query.filter_by(email=email).all()
    return render_template("clpolicy.html",data=q)

if __name__=="__main__":
    app.run(debug=True)