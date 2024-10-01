import unittest
import os

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import Department, Employee, Role


class TestBase(TestCase):

    def create_app(self):

        #Pasar las configuraciones de prueba.
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://em_admin:em2020@localhost/em_test'
        )
        return app

    def setUp(self):
        """
       Será llamado antes de cada prueba.
        """

        db.create_all()

        # crear usuario administrador de prueba
        admin = Employee(username="admin", password="admin2020", is_admin=True)

        #crear usuario de prueba no administrador
        employee = Employee(username="test_user", password="test2020")

        # guardar usuarios en la base de datos
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
       Será llamado después de cada prueba.
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_employee_model(self):
        """
       Número de prueba de registros en la tabla de empleados
        """
        self.assertEqual(Employee.query.count(), 2)

    def test_department_model(self):
        """
       Número de prueba de registros en la tabla Departamento
        """

        # crear departamento de pruebas
        department = Department(name="IT", description="The IT Department")

        # guardar departamento en base de datos
        db.session.add(department)
        db.session.commit()

        self.assertEqual(Department.query.count(), 1)

    def test_role_model(self):
        """
        Test number of records in Role table
        """

        # crear rol de prueba
        role = Role(name="CEO", description="Run the whole company")

        # guardar rol en la base de datos
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)


class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Pruebe que se pueda acceder a la página de inicio sin iniciar sesión
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
       Pruebe que se pueda acceder a la página de inicio de sesión sin iniciar sesión
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Pruebe que el enlace de cierre de sesión sea inaccesible sin iniciar sesión
        y redirige a la página de inicio de sesión y luego a cerrar sesión
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
       Pruebe que el panel sea inaccesible sin iniciar sesión
        y redirige a la página de inicio de sesión y luego al panel de control
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Pruebe que el panel sea inaccesible sin iniciar sesión
        y redirige a la página de inicio de sesión y luego al panel de control
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_departments_view(self):
        """
        Pruebe que la página de departamentos sea inaccesible sin iniciar sesión
        y redirige a la página de inicio de sesión y luego a la página de departamentos
        """
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        """
        Pruebe que la página de roles sea inaccesible sin iniciar sesión
        y redirige a la página de inicio de sesión y luego a la página de roles
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_view(self):
        """
        Pruebe que la página de empleados sea inaccesible sin iniciar sesión
        y redirige a la página de inicio de sesión y luego a la página de empleados
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
