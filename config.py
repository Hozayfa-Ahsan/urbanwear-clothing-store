import os


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-this-later"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///store.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False