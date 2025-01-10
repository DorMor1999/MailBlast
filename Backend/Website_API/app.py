import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from routes.users_routes import AllUsers, Auth, UserById
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
api = Api(app)

# Get the full database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure Flask to use PostgreSQL (Neon DB) using the connection string from .env
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable Flask-SQLAlchemy event system

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# resources

#user resources
api.add_resource(AllUsers, "/api/users/")
api.add_resource(Auth, "/api/users/auth/")
api.add_resource(UserById, "/api/users/<int:user_id>")


if __name__ == "__main__":
    app.run(debug=True)