from flask import current_app as app

from . import db
from .testing.factories import UserFactory, ItemFactory, LocationFactory
from .utils import disable_on_production


@app.cli.command("yo")
def yo():
    print('yo')


@app.cli.command("populate_db")
@disable_on_production
def populate_db():

    user_factory = UserFactory()
    item_factory = ItemFactory()
    location_factory = LocationFactory()

    for _ in range(20):
        user_factory.generate().save_to_db()
        item_factory.generate().save_to_db()
        location_factory.generate().save_to_db()

    print('Population succeeded.')
    return True


@app.cli.command("flush_db")
@disable_on_production
def flush_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    print('Database flushed successfully.')
    return True
