from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


app = Flask(__name__)
app.secret_key = "lasjkflksdfjalskfj"

@app.route("/", methods=["GET", "POST"])
def home():
    form = OrderForm()
    
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        print(first_name, last_name, email)


    return render_template("index.html", form=form)


# set FLASK_DEBUG=on


class OrderForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=55)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    submit = SubmitField("Convert2")