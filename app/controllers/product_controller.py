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
