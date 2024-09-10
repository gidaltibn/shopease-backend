from . import db

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Chave estrangeira para Product
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
