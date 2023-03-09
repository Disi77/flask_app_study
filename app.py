from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
import json


app = Flask(__name__)
app.secret_key = "lasjkflksdfjalskfj"

PRODUCTS = [
    {"id": "p1", "name": "Apple", "price": 50},
    {"id": "p2", "name": "Pear", "price": 40},
    {"id": "p3", "name": "Orange", "price": 30}, 
    {"id": "p4", "name": "Tangerine", "price": 20}, 
    {"id": "p5", "name": "Plum", "price": 10}  
]


class OrderForm(FlaskForm):
    first_name = StringField("First name:", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last name:", validators=[DataRequired(), Length(min=2, max=55)])
    email = StringField("Email:", validators=[DataRequired(), Email()])

    products_choices = [(item["id"], f'{item["name"]} ({item["price"]} Kč)') for item in PRODUCTS]

    product = SelectField("Favorite product:", choices=products_choices)
    quantity = IntegerField("Quantity:", validators=[DataRequired(), NumberRange(min=1, max=20)])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = OrderForm()

    if form.validate_on_submit():
        pass
        # first_name = form.first_name.data
        # last_name = form.last_name.data
        # email = form.email.data
        # print(first_name, last_name, email)

    return render_template("index.html", form=form, products=json.dumps(PRODUCTS))
