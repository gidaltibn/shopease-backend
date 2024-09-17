import requests
from flask import Blueprint, request, jsonify
from app.models import Cart, CartItem, db
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart or not cart.items:
        return jsonify({'message': 'Cart is empty'}), 200

    cart_items = [{'product_id': item.product_id, 'quantity': item.quantity} for item in cart.items]
    return jsonify({'items': cart_items}), 200

# Rota para adicionar um produto ao carrinho
@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Fazer a requisição à FakeStore API
    try:
        response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Failed to connect to FakeStore API', 'error': str(e)}), 500

    # Verificar se a resposta foi bem-sucedida
    if response.status_code != 200:
        return jsonify({'message': f"Product with ID {product_id} not found in FakeStore API"}), 404

    # Tentar decodificar a resposta JSON
    try:
        product = response.json()
    except ValueError:
        return jsonify({'message': 'Failed to parse response from FakeStore API'}), 500

    # Verificar se o carrinho já existe, senão criar um novo
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    # Verificar se o produto já está no carrinho
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        'message': f"Product '{product['title']}' added to cart",
        'product': product['title'],
        'quantity': cart_item.quantity
    }), 200
    
@cart_bp.route('/update', methods=['POST'])
@jwt_required()
def update_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Verificar se o carrinho do usuário existe
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404

    # Verificar se o produto está no carrinho
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({'message': 'Cart updated'}), 200
    else:
        return jsonify({'message': 'Product not found in cart'}), 404


@cart_bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')

    # Verificar se o carrinho do usuário existe
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404

    # Verificar se o produto está no carrinho
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart'}), 200
    else:
        return jsonify({'message': 'Product not found in cart'}), 404
