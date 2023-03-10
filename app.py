from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
import json
from rates import get_rates


app = Flask(__name__)
app.secret_key = "lasjkflksdfjalskfj"

PRODUCTS = [
    {"id": "p1", "name": "Apple", "price": 50},
    {"id": "p2", "name": "Pear", "price": 40},
    {"id": "p3", "name": "Orange", "price": 30}, 
    {"id": "p4", "name": "Tangerine", "price": 20}, 
    {"id": "p5", "name": "Plum", "price": 10}  
]
VAT_RATE = 20

class OrderForm(FlaskForm):
    first_name = StringField("First name:", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last name:", validators=[DataRequired(), Length(min=2, max=55)])
    email = StringField("Email:", validators=[DataRequired(), Email()])

    products_choices = [(item["id"], f'{item["name"]} ({item["price"]} Kč)') for item in PRODUCTS]
    product = SelectField("Favorite product:", choices=products_choices)
    
    quantity = IntegerField("Quantity:", validators=[DataRequired(), NumberRange(min=1, max=20)])
    
    rates_data = get_rates()["rates"]
    rates_choices = [item["code"] for item in rates_data] 
    rate = SelectField("Convert to:", choices=["---"] + rates_choices)

    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = OrderForm()
    results = None

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        product_id = form.product.data
        for item in PRODUCTS:
            if item["id"] == product_id:
                product_name = item["name"]
                product_price = item["price"]
        quantity = form.quantity.data
        rate_code = form.rate.data

        rates = get_rates()
        if rate_code == "---":
            rate_amount = rate = 1
            rate_code = "CZK"
        else:
            for item in rates["rates"]:
                if item["code"] == rate_code:
                    rate_amount = item["amount"]
                    rate = item["rate"]
        
        subtotal = product_price * quantity
        vat = round(VAT_RATE / 100 * subtotal, 2)
        subtotal_with_price = subtotal + vat
        converted_price = round((rate_amount * subtotal_with_price) / rate, 2)

        results = {"first_name": first_name,
                   "last_name": last_name,
                   "email": email,
                   "product_id": product_id,
                   "product_name": product_name,
                   "product_price": product_price,
                   "quantity": quantity,
                   "subtotal": subtotal,
                   "rate_code": rate_code,
                   "vat": vat,
                   "vat_rate": VAT_RATE,
                   "product_price_with_vat": subtotal_with_price,
                   "converted_price": converted_price}


    return render_template("index.html", form=form, products=json.dumps(PRODUCTS), summary=results)
