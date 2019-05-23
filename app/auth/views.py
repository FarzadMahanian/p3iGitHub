# app/auth/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    if not current_user.is_admin:
        abort(403)
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            name=form.name.data,
                            role=form.role.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """

    if Employee.query.count() == 0:
        employee = Employee(email='admin@polito.it',
                            username='admin_user',
                            name='Admin User',
                            role='CEO',
                            password='admin123')

        # add employee to the database
        db.session.add(employee)
        db.session.commit()

    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the dashboard page after login
            return redirect(url_for('home.list_products'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('home.list_products'))
