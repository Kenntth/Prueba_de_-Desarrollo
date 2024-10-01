# Prueba de desarrollo CRUD

---

# 

Este proyecto es una aplicación web para la gestión de empleados, desarrollada utilizando **Flask** como framework backend y **MySQL** como base de datos. Proporciona funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) para empleados y departamentos.

## Tecnologías Utilizadas

- **Flask**: Microframework para la construcción de aplicaciones web en Python.
- **Flask-SQLAlchemy**: Extensión de Flask que facilita la interacción con la base de datos mediante el uso de un ORM (Object-Relational Mapping).
- **MySQL**: Sistema de gestión de bases de datos relacional utilizado para almacenar los datos de empleados y departamentos.
- **Flask-Migrate**: Herramienta para gestionar las migraciones de base de datos y aplicar cambios en el esquema.
- **Flask-Login**: Extensión para gestionar la autenticación de usuarios (inicio y cierre de sesión).
- **HTML/CSS**: Para la interfaz de usuario.

## Requisitos

Antes de iniciar, asegúrate de tener instalados los siguientes requisitos:

- Python 2.7 o superior
- MySQL Server
- Anaconda (opcional, pero recomendado para gestionar entornos virtuales)

## Instalación

```

### 2. Crear un entorno virtual

Si usas **Anaconda**, puedes crear un entorno virtual con Python 2.7:

```bash
conda create -n flaskenv python=2.7 anaconda
conda activate flaskenv
```

### 3. Instalar dependencias

Instala las dependencias del proyecto utilizando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos MySQL

1. Inicia sesión en MySQL:
   ```bash
   mysql -u root -p
   ```

2. Crea un usuario y una base de datos:

   ```sql
   CREATE USER 'em_admin'@'localhost' IDENTIFIED BY 'em2020';
   CREATE DATABASE emp_db;
   GRANT ALL PRIVILEGES ON emp_db.* TO 'em_admin'@'localhost';
   ```

### 5. Migraciones de Base de Datos

Inicializa las migraciones y crea el esquema de base de datos:

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Ejecutar la aplicación

Una vez configurada la base de datos, puedes ejecutar la aplicación:

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000/`.

## Funcionalidades

- Listar empleados y departamentos.
- Agregar, editar y eliminar empleados.
- Gestión de departamentos.
- Autenticación de usuarios con **Flask-Login**.


