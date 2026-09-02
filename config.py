import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-this-later"
    )

    # =====================================================
    # DATABASE
    # =====================================================

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    if DATABASE_URL:

        # Render PostgreSQL may provide postgres://
        # SQLAlchemy expects postgresql://

        if DATABASE_URL.startswith("postgres://"):

            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    else:

        # Local development database

        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///store.db"
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False