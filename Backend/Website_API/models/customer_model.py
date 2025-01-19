from app import db

class Customer(db.Model):
    __tablename__ = 'customers'  # Name of the table in the database
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120))
    city = db.Column(db.String(120))
    birthday = db.Column(db.Date)

    def __repr__(self):
        return (f"<Customer customer_id={self.customer_id}, "
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"email='{self.email}', "
                f"country='{self.country}', "
                f"city='{self.city}', "
                f"birthday={self.birthday}>")

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'country': self.country,
            'city': self.city,
            'birthday': self.birthday.isoformat() if self.birthday else None
        }