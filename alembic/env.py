from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, MetaData, pool
from logging.config import fileConfig

import os,sys
sys.path.append(os.getcwd())
from application import DevelopmentConfig
from application.models import metadata_declarative
from application.models_tables import metadata_classical

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

alembic_config.set_main_option('sqlalchemy.url', DevelopmentConfig.DATABASE_URI)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(alembic_config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
our_metadata = MetaData()

all_metadatas = [metadata_classical, metadata_declarative]
for metadata in all_metadatas:
    for t in metadata.tables.values():
        t.tometadata(our_metadata)


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    engine = engine_from_config(
        alembic_config.get_section(
            alembic_config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=our_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

