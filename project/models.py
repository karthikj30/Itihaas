from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Add other user fields

class TourPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    duration = db.Column(db.String(50))
    includes = db.Column(db.Text)
    state = db.Column(db.String(100))
    guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))

class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    rating = db.Column(db.Float)
    experience = db.Column(db.String(50))
    languages = db.Column(db.String(200))
    description = db.Column(db.Text)

class Merchandise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    category = db.Column(db.String(50))  # e.g., 'clothing', 'accessories', 'souvenirs'
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandise.id'))
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered
    shipping_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandise.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)  # Price at the time of purchase 