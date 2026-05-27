import pymysql
from flask import g, current_app

def get_db():
    """获取数据库连接（存储在Flask的g对象中，同一请求复用）"""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            port=current_app.config['MYSQL_PORT'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB'],
            charset=current_app.config['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """注册数据库关闭函数到Flask应用"""
    app.teardown_appcontext(close_db)

def execute_query(sql, params=None, fetchone=False):
    """执行查询语句并返回结果"""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()

def execute_insert(sql, params=None):
    """执行插入语句并返回最后插入的ID"""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        db.commit()
        return cursor.lastrowid

def execute_update(sql, params=None):
    """执行更新语句并返回影响的行数"""
    db = get_db()
    with db.cursor() as cursor:
        result = cursor.execute(sql, params)
        db.commit()
        return result

def execute_many(sql, params_list):
    """批量执行语句"""
    db = get_db()
    with db.cursor() as cursor:
        result = cursor.executemany(sql, params_list)
        db.commit()
        return result
