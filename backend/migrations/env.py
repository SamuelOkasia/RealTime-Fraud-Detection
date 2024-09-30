from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.utils.database import Base  # Base class for model definitions
from app.utils.models import Transaction  # Import model (Transaction) to be included in migrations
from app.utils.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST  # Load PostgreSQL credentials

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Configure the database URL dynamically using environment variables for PostgreSQL
config.set_main_option('sqlalchemy.url', f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}')

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Metadata object to keep track of models (used by Alembic for schema migration).
target_metadata = Base.metadata

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    In offline mode, SQLAlchemy generates the migration scripts without connecting
    to the database. It uses the SQLAlchemy URL to generate the necessary SQL statements.
    """
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),  # Use the database URL
        target_metadata=target_metadata,  # Apply the migration to all models' metadata
        literal_binds=True,  # Use literal values for SQL parameters
        dialect_opts={"paramstyle": "named"},  # Specify parameter style for the SQL dialect
    )

    # Begin the migration transaction
    with context.begin_transaction():
        context.run_migrations()  # Apply the migration scripts

def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In online mode, Alembic connects to the database and directly applies the migration.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # Read configuration section for SQLAlchemy engine
        prefix="sqlalchemy.",  # Use 'sqlalchemy.' prefix for configuration options
        poolclass=pool.NullPool,  # Use NullPool to avoid connection pooling during migration
    )

    # Connect to the database and apply the migration
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)  # Set up connection and metadata

        with context.begin_transaction():
            context.run_migrations()  # Apply the migration scripts

# Determine whether to run migrations in 'offline' or 'online' mode based on the Alembic context
if context.is_offline_mode():
    run_migrations_offline()  # Run offline migration
else:
    run_migrations_online()  # Run online migration
