import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

def check_token(token: str):
    """
    Return None if check ok
    Return dic and status code if error
    """
    if not token:
        return {"message": "Access denied. Token required."}, 401

    # Remove "Bearer " if it's included in the token string
    token = token.replace('Bearer ', '')

    #get key from env
    load_dotenv()
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")
    
    # Decode and verify the JWT token
    try:
        decoded_token = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
        user_id = decoded_token['user_id']  # Assuming the token contains 'user_id'
    except jwt.ExpiredSignatureError:
        return {"message": "Token has expired."}, 401
    except jwt.InvalidTokenError:
        return {"message": "Invalid token."}, 401
    

def get_new_token(email: str, user_id: int)-> str:
        """Generate token for 3 hours and return it."""
        # Generate JWT token
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=3)  # Token expires in 3 hour
        }
        load_dotenv()
        jwt_secret_key = os.getenv("JWT_SECRET_KEY")
        token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")
        return token