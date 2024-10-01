from __future__ import with_statement

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# este es el objeto Alembic Config, que proporciona
# acceso a los valores dentro del archivo .ini en uso.
config = context.config

# Interprete el archivo de configuración para el registro de Python.
# Esta línea configura básicamente los registradores.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# agregue el objeto MetaData de su modelo aquí
# para soporte de 'generación automática'
# desde myapp importar mymodel
# target_metadata = mimodelo.Base.metadata
from flask import current_app
config.set_main_option(
    'sqlalchemy.url', current_app.config.get(
        'SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata



def run_migrations_offline():
    """Ejecute migraciones en modo 'fuera de línea'.

    Esto configura el contexto con solo una URL.
    y no un motor, aunque un motor es aceptable
    aquí también.  Saltándose la creación del motor
    ni siquiera necesitamos que un DBAPI esté disponible.

    Las llamadas a context.execute() aquí emiten la cadena dada al
    salida del guión.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """

    """

    # Esta devolución de llamada se utiliza para evitar que se genere una migración automática.
    # cuando no hay cambios en el esquema
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
