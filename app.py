import os
from flask import Flask
from sqlalchemy import URL
from models import db
from controllers.login import login_bp
from dotenv import load_dotenv

load_dotenv(override=True)

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT", 3306)),
        database=os.getenv("DATABASE")
    )

    key = os.getenv("SECRET_KEY")
    if not key:
        raise ValueError("SECRET_KEY no está definida")

    app.config["SECRET_KEY"] = key
    db.init_app(app)

    app.register_blueprint(login_bp, url_prefix="/")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)