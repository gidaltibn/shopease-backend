import requests
from flask import Blueprint, jsonify

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    response = requests.get('https://fakestoreapi.com/products')
    
    if response.status_code != 200:
        return jsonify({'message': 'Failed to fetch products from FakeStore API'}), 500

    products = response.json()
    return jsonify(products), 200

# Rota para buscar um produto pelo ID
@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
    
    if response.status_code != 200:
        return jsonify({'message': f'Product with ID {product_id} not found in FakeStore API'}), 404

    product = response.json()
    return jsonify(product), 200

