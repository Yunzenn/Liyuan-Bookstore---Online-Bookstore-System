from flask import Flask
from app.config import Config

def create_app():
    """Flask应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化数据库
    from app import database
    database.init_app(app)

    # 注册蓝图
    from app.routes import auth, books, orders
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(orders.bp)

    # 注册主路由
    @app.route('/')
    def index():
        from flask import render_template, session
        return render_template('index.html')

    return app
