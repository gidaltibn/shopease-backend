from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    # Relacionamento com OrderItem
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
