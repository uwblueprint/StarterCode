import os
import sys
sys.path.append('..')
sys.path.append('../..')

from csv import reader


def _get_data():
    filepath = os.path.join(os.getcwd(), 'backend/db/StarterCodeSampleData.csv')
    with open(filepath) as data:
        csv_reader = reader(data)

        header = [column.lower() for column in next(csv_reader)]
        return [zip(header, row) for row in csv_reader]


def _init_postgres_db(app):
    from . import db
    from .models import RecycledMaterial

    # See http://flask-sqlalchemy.pocoo.org/latest/contexts/
    app.app_context().push()
    db.init_app(app)

    # Clear database tables
    db.reflect()
    db.drop_all()

    # Init database tables
    db.create_all()

    # Seed database with sample data
    data = _get_data()
    for row in data:
        db.session.add(RecycledMaterial(**dict(row)))
    db.session.commit()


def init_db(app):
    _init_postgres_db(app)
