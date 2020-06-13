import datetime as dt

from . import db


class TimestampMixin:
    created = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, server_default=str(dt.datetime.utcnow()))
    modified = db.Column(db.DateTime, onupdate=dt.datetime.utcnow)


class NModel(db.Model):
    __abstract__ = True

    def save_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
        return self
