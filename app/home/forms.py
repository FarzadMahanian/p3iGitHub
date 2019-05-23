# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, ValidationError, SelectField, FloatField
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Product, Supplier, Shipment


class ProductForm(FlaskForm):
    """
    Form to add or edit a Product
    """
    name = StringField('Name', validators=[DataRequired()])
    mfg_date = DateField('Mfg. Date', validators=[DataRequired()])
    rcv_date = DateField('Rcv. Date', validators=[DataRequired()])
    exp_date = DateField('Exp. Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    stock = FloatField('Stock', validators=[DataRequired()])
    supplier = QuerySelectField('Supplier', validators=[DataRequired()],
                                query_factory=lambda: Supplier.query.all(),
                                get_label="name")

    submit = SubmitField('Submit')


class SupplierForm(FlaskForm):
    """
    Form to add or edit a Supplier
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ShipmentForm(FlaskForm):
    """
    Form to add or edit a Supplier
    """
    product = QuerySelectField('Product', validators=[DataRequired()],
                               query_factory=lambda: Product.query.all(),
                               get_label="name")
    department = SelectField('Department', validators=[DataRequired()], choices=[('Quality', 'Quality'),
                                                                                 ('Production', 'Production'),
                                                                                 ('Other', 'Other')])
    name = StringField('Name', validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    shipment_date = DateField('Shipment Date', validators=[DataRequired()])
    submit = SubmitField('Submit')
