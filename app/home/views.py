from flask import render_template, abort
from flask_login import login_required, current_user

from . import home


@home.route('/')
def homepage():
    """
    Renderice la plantilla de la página de inicio en la ruta /
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Representar la plantilla del panel en la ruta /dashboard
    """
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    #evitar que los no administradores accedan a la página
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
