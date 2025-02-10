from flask import Flask, render_template, request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message
from pyexpat.errors import messages

app=Flask(__name__)
app.config["SECRET_KEY"]="myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///data.db"
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_USERNAME"]="niranjangowda.583@gmail.com"
app.config["MAIL_PASSWORD"]="ewbubfqjgccvybcl"

db=SQLAlchemy(app)
mail=Mail(app)

class Form(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(80))
    last_name=db.Column(db.String(80))
    email=db.Column(db.String(80))
    date=db.Column(db.Date)
    occupation=db.Column(db.String(80))


@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        first_name=request.form["first_name"]
        last_name=request.form["last_name"]
        email=request.form["email"]
        date=request.form["date"]
        date_obj=datetime.strptime(date,"%Y-%m-%d").date()
        occupation=request.form["occupation"]
        submit=request.form["submit"]

        form=Form(first_name=first_name,last_name=last_name,email=email,date=date_obj,occupation=occupation)
        db.session.add(form)
        db.session.commit()
        messages=(f"Thank you for your submission, {first_name}\n"
                  f"here are your data:{first_name}\t{last_name}\n{date}\n"
                  f"Thank you")
        message=Message(subject="New message submission",sender=app.config["MAIL_USERNAME"],
                        recipients=[email],body=messages)

        flash("Your form was submitted successfully","success")
        mail.send(message)

    return render_template('index.html')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True,port=5001)
