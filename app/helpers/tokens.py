import jwt
from app.config import PROJECT_SECRET


def encrypt_data(data):
    """Encrypt the data to JWT Token"""
    encoded_jwt = jwt.encode(data, PROJECT_SECRET, algorithm="HS256")

    return encoded_jwt


def decrypt_token(received_token):
    """Decrypt the token and return data"""
    # Get JWT Token
    token = received_token
    if not token:
        # If token is missing
        return None
    # Decode the JWT Token with Project Secret Key
    data = jwt.decode(token, PROJECT_SECRET, algorithms=["HS256"])
    return data
