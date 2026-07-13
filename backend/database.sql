-- Create Database
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description LONGTEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    category VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_name (name)
);

-- Cart Table
CREATE TABLE IF NOT EXISTS cart (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user_id (user_id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_order_id (order_id)
);

-- Insert sample data
INSERT INTO products (name, description, price, stock, category, image_url) VALUES
('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 10, 'Electronics', 'https://via.placeholder.com/300?text=Laptop+Pro'),
('Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 29.99, 50, 'Accessories', 'https://via.placeholder.com/300?text=Wireless+Mouse'),
('USB-C Cable', 'High-speed USB-C charging and data transfer cable', 12.99, 100, 'Accessories', 'https://via.placeholder.com/300?text=USB-C+Cable'),
('Mechanical Keyboard', 'RGB mechanical keyboard for gaming and typing', 99.99, 25, 'Accessories', 'https://via.placeholder.com/300?text=Mechanical+Keyboard'),
('4K Monitor', '27-inch 4K monitor with HDR support', 399.99, 15, 'Electronics', 'https://via.placeholder.com/300?text=4K+Monitor'),
('Webcam HD', '1080p HD webcam with microphone', 49.99, 40, 'Accessories', 'https://via.placeholder.com/300?text=Webcam+HD'),
('External SSD', '1TB external solid state drive', 149.99, 20, 'Storage', 'https://via.placeholder.com/300?text=External+SSD'),
('Phone Stand', 'Adjustable phone and tablet stand', 19.99, 60, 'Accessories', 'https://via.placeholder.com/300?text=Phone+Stand');
