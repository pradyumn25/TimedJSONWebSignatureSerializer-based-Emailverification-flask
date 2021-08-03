from logging import error
from types import MethodType
from flask import Flask,render_template, request, redirect
from flask.globals import session
from flask.templating import render_template_string
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = 'super_secret_key'

local_server =  "True"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/mofit"
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "pundirdemo@gmail.com",
    MAIL_PASSWORD=  "Par@12345"
)

s = Serializer('sekrit', expires_in=300)

mail = Mail(app)

class Signup(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), unique=False, nullable=False)
    last = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(80),  nullable=False)



@app.route("/") #home page------------------------
def index():
    return render_template('index.html')

@app.route("/logout")  #logout
def logout():
    session.pop('email')
    return render_template('signin.html')


@app.route("/signup",methods = ['GET', 'POST'])   #sign up------------------------
def signup():
    details = Signup.query.filter_by().all()

    if (request.method == 'POST'):
        code = request.form.get('code')
        email = request.form.get('email')
        if(s.loads(code) == email):

            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            password = request.form.get('pass')

            for details in details:
                if(details.email == email):
                    error = "You are already Registered"
                    return render_template('signup.html',error=error)
                    break
                else:
                    error = "You are Now Registered Please Sign In"

            if(error == "You are Now Registered Please Sign In"):
                entry = Signup(first=first_name, last=last_name,password = password, email=email)
                db.session.add(entry)
                db.session.commit()
                return render_template('signup.html',error=error)

        else:
            token_status = "Wrong Token Or Email Already Registered Please Renter Email-Address"
            return render_template('id_check.html', token_status= token_status)
        

    return render_template('signup.html')

@app.route("/signin",methods = ['GET', 'POST'])   #sign in---------------------------
def signin():
    if (request.method == 'POST'):
        details = Signup.query.filter_by().all()

        email = request.form.get('email')
        password = request.form.get('password')
        
        for details in details:
            if(details.email == email and details.password == password):
                status = "Ok"
                session['email'] = details.email
                break
            else:
                status = "Provide Right Details"

        if(status == "Provide Right Details"):
            return render_template('signin.html',status=status)

        elif(status == "Ok"):
            return render_template('dashboard.html',ss = session['email'])

        

    return render_template('signin.html')


@app.route('/id_check',methods=['GET','POST']) 
def id_check():

    if (request.method == 'POST'):
        id_check_email = request.form.get('id_check_email')
        details = Signup.query.filter_by().all()

        for details in details:
            if(id_check_email == details.email):
                error = 'Email-id Already Registered'
                break
            else:
                error = 'A verification link has been sent to your Email-id'

        if(error == 'Email-id Already Registered'):
            return render_template('id_check.html',id_check_error=error)

        else:
            token = s.dumps(id_check_email)
            token = token.decode("utf-8") 

            mail.send_message('New Message From '+ 'Mo-fit',
                            sender='pundirdemo@gmail.com',
                            recipients = ['pundirpradyumn25@gmail.com'],
                            body="please copy this token ==> " +  token + " (valid for 5 minutes only) "
                            )

            return redirect('signup')

    return render_template('id_check.html')


@app.route("/forgot", methods=['GET','POST'])
def forgot():

    if (request.method == 'POST'):
        email = request.form.get('email')
        details = Signup.query.filter_by().all()

        for details in details:
            if (email == details.email):
                token = s.dumps(email)
                token = token.decode("utf-8") 

                mail.send_message('New Message From '+ 'Mo-fit',
                                sender='pundirdemo@gmail.com',
                                recipients = ['pundirpradyumn25@gmail.com'],
                                body="please copy this token ==> " +  token + " (valid for 5 minutes only) "
                                )
                
                return redirect('reset_pass')
                break
            else:
                error = "You are not Registered"

        if(error == "You are not Registered"):
            return render_template("forgot.html", error=error)

        else:
            pass

    return render_template('forgot.html')

@app.route("/reset_pass", methods=['GET','POST'])
def reset_pass():

    if (request.method == 'POST'):

        code = request.form.get('verify')
        email = request.form.get('email')
        password = request.form.get('new_pass')

        if(s.loads(code) == email):
            details = Signup.query.filter_by(email)
            details.password = password
            db.session.commit()

            return render_template('success.html')
        else:
            error = 'Verifaication Code Error Retry'
            return render_template('forgot.html', reset_error = error)


    return render_template("reset_pass.html")

        
app.run(debug=True)