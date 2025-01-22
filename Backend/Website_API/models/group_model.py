from app import db
from models.user_model import User

class Group(db.Model):
    __tablename__ = 'groups'  # Name of the table in the database
    group_id = db.Column(db.Integer, primary_key=True)
    group_admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    group_name = db.Column(db.String(120), nullable=False)
    group_description = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    created_at_time = db.Column(db.Time, nullable=False)  
    
    # Relationship with User
    user = db.relationship('User', backref='groups', lazy=True)

    def __repr__(self):
        return (f"<Group group_id={self.group_id}, "
                f"group_admin_id={self.group_admin_id}, "
                f"group_name='{self.group_name}', "
                f"group_description='{self.group_description}', "
                f"created_at={self.created_at}, "
                f"created_at_time={self.created_at_time}>")

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'group_admin_id': self.group_admin_id,
            'group_name': self.group_name,
            'group_description': self.group_description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_at_time': self.created_at_time.isoformat() if self.created_at_time else None
        }