from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, Cart, Product, User
from auth import admin_required

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    return jsonify({
        'orders': [order.to_dict() for order in orders],
        'total': len(orders)
    }), 200


@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict()), 200


@order_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create order from cart"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Get user's cart
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create order
    order = Order(user_id=user_id, total_price=total_price, status='pending')
    db.session.add(order)
    db.session.flush()  # Flush to get order ID
    
    # Add order items from cart
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        # Decrease product stock
        cart_item.product.stock -= cart_item.quantity
        db.session.add(order_item)
    
    # Clear cart
    Cart.query.filter_by(user_id=user_id).delete()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict()
    }), 201


@order_bp.route('/<int:order_id>', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status (admin only)"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered']
    status = data.get('status')
    
    if status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of {valid_statuses}'}), 400
    
    order.status = status
    db.session.commit()
    
    return jsonify({
        'message': 'Order status updated',
        'order': order.to_dict()
    }), 200


@order_bp.route('', methods=['GET'])
@admin_required
def get_all_orders():
    """Get all orders (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    paginated = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'orders': [order.to_dict() for order in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200
