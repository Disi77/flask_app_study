from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange


app = Flask(__name__)
app.secret_key = "lasjkflksdfjalskfj"


class OrderForm(FlaskForm):
    first_name = StringField("First name:", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last name:", validators=[DataRequired(), Length(min=2, max=55)])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    product = SelectField("Favorite product:", choices=[('p1', 'Product 1 (500 Kč)'), ('p2', 'Product 2 (1.000 Kč)'), ('p3', 'Product 3 (1.500 Kč)')])
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

    return render_template("index.html", form=form)
