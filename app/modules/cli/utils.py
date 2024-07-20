from werkzeug.security import generate_password_hash

from app.extensions.db import db
from app.modules.auth.schemas import SignUpRequestSchema
from app.modules.user.models import UserModel


def create_admin(username, email, password):
    # Validate data using SignUpRequestSchema
    user_data = {"username": username, "email": email, "password": password}
    schema = SignUpRequestSchema()
    errors = schema.validate(user_data)
    if errors:
        raise ValueError(errors)

    # Create new admin user
    new_admin = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        password=generate_password_hash(
            password=user_data["password"], method="pbkdf2:sha256"
        ),
        role="admin",
    )
    db.session.add(new_admin)
    db.session.commit()

    return new_admin
