# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(60))

    @property
    def is_admin(self):
        return self.role in ['CEO', 'Manager']

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Product(db.Model):
    """
    Create a Product table
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    mfg_date = db.Column(db.Date)
    exp_date = db.Column(db.Date)
    rcv_date = db.Column(db.Date)
    location = db.Column(db.String(100))
    stock = db.Column(db.Float)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    shipments = db.relationship('Shipment', backref='product', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='product', lazy='dynamic')

    def __repr__(self):
        return '<Product: {}>'.format(self.name)


class Supplier(db.Model):
    """
    Create a Supplier table
    """

    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60), index=True, unique=True)
    contact = db.Column(db.String(50))
    address = db.Column(db.String(100))
    products = db.relationship('Product', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return '<Supplier: {}>'.format(self.name)


class Shipment(db.Model):
    """
    Create a Shipment table
    """

    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(60))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Float)
    shipment_date = db.Column(db.Date)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return '<Shipment: {} units of {} sent to {} from {} on {}>'.format(self.quantity,
                                                                            self.product_id,
                                                                            self.name,
                                                                            self.department,
                                                                            self.shipment_date)


class Transaction(db.Model):
    """
    Create a Transaction table
    """

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    date = db.Column(db.Date)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'product': self.product.name,
            'quantity': self.quantity
        }

    def __repr__(self):
        return '<Transaction: {} units of {} sent/received>'.format(self.quantity,
                                                                    self.product_id)
