from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
   Manejar solicitudes a la ruta /register
    Agregar un empleado a la base de datos a través del formulario de registro
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # agregar empleado a la base de datos
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirigir a la página de inicio de sesión
        return redirect(url_for('auth.login'))

    # cargar plantilla de registro
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
   Manejar solicitudes a la ruta /login
    Inicie sesión como empleado a través del formulario de inicio de sesión
    """
    form = LoginForm()
    if form.validate_on_submit():

        # comprobar si el empleado existe en la base de datos y si
        # la contraseña ingresada coincide con la contraseña en la base de datos
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # registrar al empleado
            login_user(employee)

            # redirigir a la página del panel correspondiente
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # cuando los datos de inicio de sesión son incorrectos
        else:
            flash('Invalid email or password.')

    # cargar plantilla de inicio de sesión
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
   Manejar solicitudes a la ruta /logout
    Cerrar la sesión de un empleado a través del enlace de cierre de sesión
    """
    logout_user()
    flash('Has cerrado sesión correctamente.')

    # redirigir a la página de inicio de sesión
    return redirect(url_for('auth.login'))
