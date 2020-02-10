import os
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from items.routes import items_bp


load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.register_blueprint(items_bp)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def indexs():
    return "Neighborrow."


if __name__ == "__main__":
    app.run()
