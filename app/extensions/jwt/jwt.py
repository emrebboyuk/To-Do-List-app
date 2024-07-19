from flask_jwt_extended import JWTManager
from app.modules.user.models import UserModel
from flask import jsonify

jwt = JWTManager()


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.query.get(identity)
    return {"role": user.role}


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )
