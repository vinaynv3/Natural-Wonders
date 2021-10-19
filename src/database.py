
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db():
    if 'db' not in g:
        g.db = db
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.session.close()


@click.command('drop_db')
@with_appcontext
def destruct_db_command():
    """Deletes data and tables."""
    get_db().init_app(current_app)
    get_db().drop_all()
    click.echo('Database Dropped')


@click.command('init_db')
@with_appcontext
def init_db_command():
    """Creates data and new tables."""
    from .models import Locations
    get_db().init_app(current_app)
    get_db().create_all()
    click.echo('Database Initialized')


def init_db(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(destruct_db_command)
    with app.app_context():
        get_db().init_app(current_app)
