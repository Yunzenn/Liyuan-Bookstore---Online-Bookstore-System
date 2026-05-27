import os

class Config:
    """Flask应用配置"""
    # 密钥（用于session加密）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'online-bookstore-secret-key-2024'

    # MySQL数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'online_bookstore'
    MYSQL_CHARSET = 'utf8mb4'

    # 分页配置
    BOOKS_PER_PAGE = 12
    ORDERS_PER_PAGE = 10
