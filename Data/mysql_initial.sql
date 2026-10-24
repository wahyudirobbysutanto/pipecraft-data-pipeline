USE bizpulse_db;

CREATE TABLE IF NOT EXISTS daily_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trx_date DATE NOT NULL,
    total_trx INT NOT NULL,
    total_revenue DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS top_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trx_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    qty_sold INT NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL
);

INSERT INTO daily_sales (trx_date, total_trx, total_revenue, payment_method) VALUES
('2026-10-20', 10, 500000.00, 'QRIS'),
('2026-10-21', 15, 750000.00, 'Credit Card'),
('2026-10-22', 8, 400000.00, 'Cash'),
('2026-10-23', 12, 600000.00, 'QRIS');

INSERT INTO top_products (trx_date, product_name, qty_sold, subtotal) VALUES
('2026-10-20', 'Kopi Susu', 20, 300000.00),
('2026-10-21', 'Roti Bakar', 15, 225000.00),
('2026-10-22', 'Es Teh', 25, 125000.00);