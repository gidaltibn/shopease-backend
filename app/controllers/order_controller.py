from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Order, OrderItem, Cart, CartItem, db
import requests

order_bp = Blueprint('order', __name__)

# Rota para listar o histórico de pedidos do usuário
@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()

    # Buscar os pedidos do usuário no banco de dados
    orders = Order.query.filter_by(user_id=user_id).all()

    # Formatar a resposta com os detalhes dos pedidos
    order_list = [
        {
            'order_id': order.id,
            'items': [{'product_id': item.product_id, 'quantity': item.quantity, 'price': item.price} for item in order.items],
            'status': order.status,
            'total_price': order.total_price
        }
        for order in orders
    ]

    return jsonify({'orders': order_list}), 200

# Rota para finalizar o pedido (checkout)
@order_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()

    # Obter o carrinho do usuário
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({'message': 'Cart is empty'}), 400

    print(f"Cart found for user {user_id} with {len(cart.items)} items.")

    # Calcular o total do pedido
    total_price = 0
    for item in cart.items:
        # Buscar o produto na FakeStore API
        response = requests.get(f'https://fakestoreapi.com/products/{item.product_id}')
        if response.status_code != 200:
            return jsonify({'message': f"Product with ID {item.product_id} not found"}), 404
        product = response.json()
        print(f"Product {product['title']} fetched from FakeStore API.")
        total_price += product['price'] * item.quantity

    print(f"Total price calculated: {total_price}")

    # Criar um novo pedido com o total calculado
    order = Order(user_id=user_id, total_price=total_price)
    db.session.add(order)
    db.session.commit()  # Fazer commit para obter o ID do pedido

    print(f"Order created with ID {order.id}")

    # Mover os itens do carrinho para o pedido
    for item in cart.items:
        response = requests.get(f'https://fakestoreapi.com/products/{item.product_id}')
        product = response.json()

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product['price']
        )
        db.session.add(order_item)
        db.session.delete(item)  # Remover os itens do carrinho

    db.session.commit()

    print(f"Order {order.id} placed successfully with {len(cart.items)} items.")

    return jsonify({
        'message': 'Order placed successfully!',
        'order_id': order.id,
        'total_items': len(cart.items),
        'total_price': total_price
    }), 200