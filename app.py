from types import MethodType
from flask import Flask,render_template, request, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '***',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "*****",
    MAIL_PASSWORD=  "******"
)

s = Serializer('sekrit', expires_in=300)

mail = Mail(app)

@app.route("/signup",methods = ['GET', 'POST'])   #sign up------------------------
def signup():
    if (request.method == 'POST'):
        code = request.form.get('code')
        email = request.form.get('email')
        if(s.loads(code) == email):
            status = "Email verification successfull"
            
    return render_template('index.html',status= status)


@app.route('/id_check',methods=['GET','POST'])  #Token generator------------------------
def id_check():
    if (request.method == 'POST'):
        id_check_email = request.form.get('id_check_email')
        token = s.dumps(id_check_email)
        token = token.decode("utf-8") 

        mail.send_message('New Message From '+ 'ABCD',
                        sender='sender emai id',
                        recipients = ['recipients email id'],
                        body="please copy this token ==> " +  token + " (valid for 5 minutes only) "
                        )

        return redirect('signup')
    return render_template('id_check.html')

app.run(debug=True)
