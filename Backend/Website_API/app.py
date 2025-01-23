import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from routes.users_routes.users_routes_resources import init_users_routes_resources
from routes.groups_routes.groups_routes_resources import init_groups_routes_resources
from routes.customers_routes.customers_routes_resources import init_customers_routes_resources

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
init_users_routes_resources(api)

#group resources
init_groups_routes_resources(api)

#customers resources
init_customers_routes_resources(api)

if __name__ == "__main__":
    app.run(debug=True)