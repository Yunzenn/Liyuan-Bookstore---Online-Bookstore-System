-- =============================================
-- 网上书店数据库 - 建表脚本
-- 数据库: online_bookstore
-- 字符集: utf8mb4
-- =============================================

-- 创建数据库
DROP DATABASE IF EXISTS online_bookstore;
CREATE DATABASE online_bookstore
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE online_bookstore;

-- =============================================
-- 1. 客户表 (customer)
-- =============================================
CREATE TABLE customer (
    customer_id     INT AUTO_INCREMENT COMMENT '客户唯一标识',
    customer_name   VARCHAR(50) NOT NULL COMMENT '客户姓名',
    address         VARCHAR(200) COMMENT '地址',
    phone           VARCHAR(20) COMMENT '电话',
    email           VARCHAR(100) NOT NULL COMMENT '邮箱',
    password_hash   VARCHAR(255) NOT NULL COMMENT '密码哈希',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (customer_id),
    UNIQUE KEY uk_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户表';

-- =============================================
-- 2. 图书表 (book)
-- =============================================
CREATE TABLE book (
    ISBN            VARCHAR(13) COMMENT 'ISBN号',
    title           VARCHAR(200) NOT NULL COMMENT '书名',
    author          VARCHAR(100) NOT NULL COMMENT '作者',
    price           DECIMAL(10,2) NOT NULL COMMENT '定价',
    publisher       VARCHAR(100) COMMENT '出版社',
    publish_year    YEAR COMMENT '出版年',
    stock           INT DEFAULT 0 COMMENT '库存数量',

    PRIMARY KEY (ISBN),
    CHECK (price >= 0),
    CHECK (stock >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='图书表';

-- =============================================
-- 3. 订单表 (order)
-- 注意: order是MySQL保留字，需要用反引号括起来
-- =============================================
CREATE TABLE `order` (
    order_id        INT AUTO_INCREMENT COMMENT '订单唯一标识',
    customer_id     INT NOT NULL COMMENT '下单客户ID',
    order_date      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
    status          ENUM('待付款','已付款','已发货','已完成','已取消') DEFAULT '待付款' COMMENT '订单状态',
    total_amount    DECIMAL(10,2) COMMENT '订单总额',

    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- =============================================
-- 4. 订单明细表 (order_item)
-- =============================================
CREATE TABLE order_item (
    order_id        INT COMMENT '订单ID',
    ISBN            VARCHAR(13) COMMENT '图书ISBN',
    quantity        INT NOT NULL COMMENT '购买数量',
    unit_price      DECIMAL(10,2) NOT NULL COMMENT '下单时单价',

    PRIMARY KEY (order_id, ISBN),
    FOREIGN KEY (order_id) REFERENCES `order`(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (ISBN) REFERENCES book(ISBN)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK (quantity > 0),
    CHECK (unit_price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单明细表';

-- =============================================
-- 5. 创建索引
-- =============================================
-- 客户表索引
CREATE INDEX idx_customer_name ON customer(customer_name);

-- 图书表索引
CREATE INDEX idx_book_title ON book(title);
CREATE INDEX idx_book_author ON book(author);

-- 订单表索引
CREATE INDEX idx_order_customer ON `order`(customer_id);
CREATE INDEX idx_order_date ON `order`(order_date);
CREATE INDEX idx_order_status ON `order`(status);
