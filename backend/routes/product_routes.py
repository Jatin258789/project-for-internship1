from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product, User
from auth import admin_required

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

@product_bp.route('', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    category = request.args.get('category')
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'products': [p.to_dict() for p in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product details"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict()), 200


@product_bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create a new product (admin only)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock', 0)
    
    if not all([name, price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    product = Product(
        name=name,
        description=data.get('description'),
        price=float(price),
        stock=int(stock),
        category=data.get('category'),
        image_url=data.get('image_url')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': product.to_dict()
    }), 201


@product_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update product (admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    if 'stock' in data:
        product.stock = int(data['stock'])
    if 'category' in data:
        product.category = data['category']
    if 'image_url' in data:
        product.image_url = data['image_url']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': product.to_dict()
    }), 200


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete product (admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200


@product_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    categories = db.session.query(Product.category).distinct().all()
    return jsonify({
        'categories': [c[0] for c in categories if c[0]]
    }), 200
