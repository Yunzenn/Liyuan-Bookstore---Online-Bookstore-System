-- =============================================
-- 网上书店数据库 - 视图定义
-- =============================================

USE online_bookstore;

-- =============================================
-- 1. 客户订单汇总视图
-- 用途：查看每个客户的订单统计
-- =============================================
CREATE VIEW v_customer_order_summary AS
SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM customer c
LEFT JOIN `order` o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email;

-- =============================================
-- 2. 订单详情视图
-- 用途：查看订单的完整信息（含客户信息）
-- =============================================
CREATE VIEW v_order_detail AS
SELECT
    o.order_id,
    o.order_date,
    o.status AS order_status,
    o.total_amount,
    c.customer_id,
    c.customer_name,
    c.email,
    c.phone,
    c.address
FROM `order` o
JOIN customer c ON o.customer_id = c.customer_id;

-- =============================================
-- 3. 订单明细详情视图
-- 用途：查看订单中每本书的详细信息
-- =============================================
CREATE VIEW v_order_item_detail AS
SELECT
    oi.order_id,
    oi.ISBN,
    b.title AS book_title,
    b.author AS book_author,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS subtotal,
    b.stock AS current_stock
FROM order_item oi
JOIN book b ON oi.ISBN = b.ISBN;

-- =============================================
-- 4. 图书销售统计视图
-- 用途：查看每本书的销售情况
-- =============================================
CREATE VIEW v_book_sales AS
SELECT
    b.ISBN,
    b.title,
    b.author,
    b.price AS current_price,
    b.stock,
    COALESCE(SUM(oi.quantity), 0) AS total_sold,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
FROM book b
LEFT JOIN order_item oi ON b.ISBN = oi.ISBN
LEFT JOIN `order` o ON oi.order_id = o.order_id AND o.status != '已取消'
GROUP BY b.ISBN, b.title, b.author, b.price, b.stock;

-- =============================================
-- 5. 热销图书视图
-- 用途：按销量排序的图书列表
-- =============================================
CREATE VIEW v_hot_books AS
SELECT
    b.ISBN,
    b.title,
    b.author,
    b.price,
    b.stock,
    COALESCE(SUM(oi.quantity), 0) AS sales_count
FROM book b
LEFT JOIN order_item oi ON b.ISBN = oi.ISBN
LEFT JOIN `order` o ON oi.order_id = o.order_id AND o.status NOT IN ('已取消', '待付款')
GROUP BY b.ISBN, b.title, b.author, b.price, b.stock
ORDER BY sales_count DESC;

-- =============================================
-- 6. 待处理订单视图
-- 用途：管理员查看需要处理的订单
-- =============================================
CREATE VIEW v_pending_orders AS
SELECT
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount,
    c.customer_name,
    c.phone,
    c.address,
    COUNT(oi.ISBN) AS item_count
FROM `order` o
JOIN customer c ON o.customer_id = c.customer_id
JOIN order_item oi ON o.order_id = oi.order_id
WHERE o.status IN ('待付款', '已付款')
GROUP BY o.order_id, o.order_date, o.status, o.total_amount,
         c.customer_name, c.phone, c.address
ORDER BY o.order_date DESC;
