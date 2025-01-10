from flask_restful import Resource
from flask import request

class UserById(Resource):
    def get(self, user_id):
        """
        Retrieve specific user by ID (requires token)
        """
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Access denied. Token required."}, 401

        return {"message": f"Retrieve user {user_id}"}, 200

    def patch(self, user_id):
        """
        Update specific user by ID (requires token)
        """
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Access denied. Token required."}, 401

        data = request.json
        return {"message": f"User {user_id} updated", "updated_fields": data}, 200
