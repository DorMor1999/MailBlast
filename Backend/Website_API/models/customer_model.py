from app import db
from models.group_model import Group
from datetime import date

class Customer(db.Model):
    __tablename__ = 'customers'  # Name of the table in the database
    customer_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id', ondelete='CASCADE'), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.Date, nullable=True)

    # Relationship to the Group model (for the customer's group)
    group = db.relationship('Group', backref='customers', lazy=True)

    def __repr__(self):
        return (f"<Customer customer_id={self.customer_id}, "
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"email='{self.email}', "
                f"country='{self.country}', "
                f"city='{self.city}', "
                f"birthday={self.birthday}, "
                f"group_id={self.group_id}>")

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'country': self.country,
            'city': self.city,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'group_id': self.group_id
        }
    
    def to_dict_with_age(self):
        """
        Converts the Customer object to a dictionary, including an additional 'age' field.

        Returns:
            dict: A dictionary representation of the Customer object with age.
        """
        calculate_age = lambda b: (date.today().year - b.year - ((date.today().month, date.today().day) < (b.month, b.day))) if b else None
        
        my_dic = self.to_dict()
        my_dic['age'] = calculate_age(self.birthday)
        return my_dic
    