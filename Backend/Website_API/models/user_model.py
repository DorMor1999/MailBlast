from app import db

class User(db.Model):
    __tablename__ = 'users'  # Name of the table in the database
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    # Relationship to the Group model (for groups the user administers)
    groups = db.relationship('Group', backref='admin', lazy=True)

    def __repr__(self):
        return f"<User user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}>"


    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
