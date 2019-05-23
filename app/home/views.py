# app/home/views.py

from flask_login import login_required, current_user
from flask import abort, flash, redirect, render_template, url_for, request
from sqlalchemy import func, case, literal_column, select
from sqlalchemy.sql import label
import pandas as pd

from app.home.forms import ProductForm, SupplierForm, ShipmentForm
from . import home
from ..models import Product, Supplier, Shipment, Transaction
from .. import db


@home.route('/')
def index():
    """
    Render the home template on the / route
    """
    return render_template('home/index.html', title="P3I")


@home.route('/products')
@login_required
def list_products():
    """
    Render the home template on the / route
    """
    products = Product.query.all()
    return render_template('home/products/list.html', products=products, title="Products")


@home.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    Add a product to the database
    """

    _add_product = True

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                          mfg_date=form.mfg_date.data,
                          exp_date=form.exp_date.data,
                          rcv_date=form.rcv_date.data,
                          location=form.location.data,
                          stock=form.stock.data,
                          supplier=form.supplier.data)
        try:
            # add product and a transaction to the database
            if product.stock <= 0:
                flash('Invalid stock entry, please enter a positive number!')
            else:
                transaction = Transaction(
                    product=product,
                    date=product.rcv_date,
                    quantity=product.stock
                )
                db.session.add(product)
                db.session.add(transaction)
                db.session.commit()
                flash('You have successfully added a new product.')
        except:
            flash('Error: An error occurred.')

        # redirect to departments page
        return redirect(url_for('home.list_products'))
    # Redirect to add supplier as we need it to add a product
    elif Supplier.query.count() == 0:
        return redirect(url_for('home.add_supplier'))

    # load product template
    return render_template('home/products/add.html', action="Add",
                           add_product=_add_product, form=form,
                           title="Add Product")


@home.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Edit a product
    """
    _add_product = False

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.mfg_date = form.mfg_date.data
        product.exp_date = form.exp_date.data
        product.rcv_date = form.rcv_date.data
        product.location = form.location.data
        product.stock = form.stock.data
        product.supplier = form.supplier.data
        db.session.commit()
        flash('You have successfully edited the product.')

        # redirect to the departments page
        return redirect(url_for('home.list_products'))

    form.name.data = product.name
    form.mfg_date.data = product.mfg_date
    form.exp_date.data = product.exp_date
    form.rcv_date.data = product.rcv_date
    form.stock.data = product.stock
    form.supplier.data = product.supplier

    return render_template('home/products/add.html', action="Edit",
                           add_product=_add_product, form=form,
                           product=product, title="Edit Product")


@home.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """
    Delete a product from the database
    """
    if not current_user.is_admin:
        abort(403)
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('You have successfully deleted the product.')

    # redirect to the departments page
    return redirect(url_for('home.list_products'))


@home.route('/suppliers')
@login_required
def list_suppliers():
    """
    Render the home template on the /suppliers route
    """
    suppliers = Supplier.query.all()
    return render_template('home/suppliers/list.html', suppliers=suppliers, title="Suppliers")


@home.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """
    Add a supplier to the database
    """

    _add_supplier = True

    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data,
                            email=form.email.data,
                            contact=form.contact.data,
                            address=form.address.data)
        try:
            # add supplier to the database
            db.session.add(supplier)
            db.session.commit()
            flash('You have successfully added a new supplier.')
        except:
            # in case supplier email already exists
            flash('Error: An error occurred.')

        # redirect to departments page
        return redirect(url_for('home.list_suppliers'))

    # load supplier template
    return render_template('home/suppliers/add.html', action="Add",
                           add_supplier=_add_supplier, form=form,
                           title="Add Supplier")


@home.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    """
    Edit a supplier
    """
    _add_supplier = False

    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.email = form.email.data
        supplier.contact = form.contact.data
        supplier.address = form.address.data
        db.session.commit()
        flash('You have successfully edited the supplier.')

        # redirect to the departments page
        return redirect(url_for('home.list_suppliers'))
    else:
        form.name.data = supplier.name
        form.email.data = supplier.email
        form.contact.data = supplier.contact
        form.address.data = supplier.address
        return render_template('home/suppliers/add.html', action="Edit",
                               add_supplier=_add_supplier, form=form,
                               supplier=supplier, title="Edit Supplier")


@home.route('/suppliers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_supplier(id):
    """
    Delete a supplier from the database
    """
    if not current_user.is_admin:
        abort(403)
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('You have successfully deleted the supplier.')

    # redirect to the departments page
    return redirect(url_for('home.list_suppliers'))


@home.route('/shipments')
@login_required
def list_shipments():
    """
    Render the home template on the /shipments route
    """
    shipments = Shipment.query.all()
    return render_template('home/shipments/list.html', shipments=shipments, title="Shipments")


@home.route('/shipments/add', methods=['GET', 'POST'])
@login_required
def add_shipment():
    """
    Add a shipment to the database
    """

    _add_shipment = True

    form = ShipmentForm()
    if form.validate_on_submit():
        shipment = Shipment(department=form.department.data,
                            name=form.name.data,
                            quantity=form.quantity.data,
                            shipment_date=form.shipment_date.data,
                            product=form.product.data)
        try:
            # add shipment to the database and update product
            product = Product.query.get_or_404(form.product.data.id)
            product.stock -= shipment.quantity
            transaction = Transaction(
                product=product,
                date=product.rcv_date,
                quantity=-shipment.quantity
            )
            if product.stock < 0 or shipment.quantity <= 0:
                flash('Specified quantity is not correct or not available')
            else:
                db.session.add(shipment)
                db.session.add(transaction)
                db.session.commit()
                flash('You have successfully added a new shipment.')
        except:
            # in case shipment already exists
            flash('Error: An error occurred.')

        # redirect to departments page
        return redirect(url_for('home.list_shipments'))

    # load shipment template
    return render_template('home/shipments/add.html', action="Add",
                           add_shipment=_add_shipment, form=form,
                           title="Add Shipment")


@home.route('/shipments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_shipment(id):
    """
    Edit a shipment
    """
    _add_shipment = False

    shipment = Shipment.query.get_or_404(id)
    form = ShipmentForm(obj=shipment)
    if form.validate_on_submit():
        old_prod = Product.query.get_or_404(shipment.product.id)
        old_prod.stock += shipment.quantity
        shipment.department = form.department.data
        shipment.name = form.name.data
        shipment.quantity = form.quantity.data
        shipment.shipment_date = form.shipment_date.data
        shipment.product = form.product.data
        new_prod = Product.query.get_or_404(shipment.product.id)
        new_prod.stock -= shipment.quantity
        if new_prod.stock < 0:
            flash('Specified quantity is not available')
        else:
            db.session.commit()
            flash('You have successfully edited the shipment.')

        # redirect to the departments page
        return redirect(url_for('home.list_shipments'))
    else:
        form.department.data = shipment.department
        form.name.data = shipment.name
        form.quantity.data = shipment.quantity
        form.shipment_date.data = shipment.shipment_date
        form.product.data = shipment.product
        return render_template('home/shipments/add.html', action="Edit",
                               add_shipment=_add_shipment, form=form,
                               shipment=shipment, title="Edit Shipment")


@home.route('/shipments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_shipment(id):
    """
    Delete a supplier from the database
    """
    if not current_user.is_admin:
        abort(403)
    shipment = Shipment.query.get_or_404(id)
    product = Product.query.get_or_404(shipment.product.id)
    product.stock += shipment.quantity
    db.session.delete(shipment)
    db.session.commit()
    flash('You have successfully deleted the shipment.')

    # redirect to the departments page
    return redirect(url_for('home.list_shipments'))


@home.route('/inventory')
@login_required
def list_inventory():
    """
    Render the home template on the /inventory route
    """
    inventory = db.session.query(Product.name, Product.location,
                         label('Quantity', func.sum(Product.stock)),
                         label('Expiry', func.min(Product.exp_date)),
                         ).group_by(Product.name, Product.location).all()
    return render_template('home/inventory/list.html', inventory=inventory, title="Inventory")


@home.route('/reports')
@login_required
def list_reports():
    """
    Render the home template on the /reports route
    """
    if not current_user.is_admin:
        abort(403)
    from_date = request.args.get('from_date', None)
    to_date = request.args.get('to_date', None)
    if from_date is None or to_date is None:
        return render_template('home/reports/list.html', transactions=pd.DataFrame(), title="Report")
    transactions = Transaction.query.filter(Transaction.date >= from_date, Transaction.date <= to_date).all()
    if len(transactions) == 0:
        return render_template('home/reports/list.html', transactions=pd.DataFrame(), title="Report")
    df = pd.DataFrame.from_records(data=[t.to_dict() for t in transactions], columns=['date', 'id', 'product', 'quantity'])
    df['in'] = df[df.quantity > 0].quantity
    df['out'] = df[df.quantity < 0].quantity
    df = df.groupby(['date', 'product'])['in', 'out'].sum()
    df.reset_index(inplace=True)

    return render_template('home/reports/list.html', transactions=df, title="Report")

