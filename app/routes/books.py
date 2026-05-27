from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from app.database import execute_query

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('/')
def book_list():
    """图书列表页面"""
    # 获取搜索参数
    keyword = request.args.get('keyword', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 12

    try:
        # 构建查询
        if keyword:
            # 搜索图书（按书名、作者、ISBN模糊匹配）
            sql = """
                SELECT * FROM book
                WHERE title LIKE %s OR author LIKE %s OR ISBN LIKE %s
                ORDER BY title
            """
            search_pattern = f'%{keyword}%'
            books = execute_query(sql, (search_pattern, search_pattern, search_pattern))

            # 获取总数
            count_sql = """
                SELECT COUNT(*) as total FROM book
                WHERE title LIKE %s OR author LIKE %s OR ISBN LIKE %s
            """
            total = execute_query(count_sql, (search_pattern, search_pattern, search_pattern), fetchone=True)['total']
        else:
            # 获取所有图书
            sql = "SELECT * FROM book ORDER BY title"
            books = execute_query(sql)
            total = len(books)

        # 手动分页（数据量小，简单处理）
        total_pages = (total + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        books_page = books[start:end]

        return render_template('books/list.html',
                             books=books_page,
                             page=page,
                             total_pages=total_pages,
                             keyword=keyword)
    except Exception as e:
        flash(f'数据库连接失败，请确保MySQL服务已启动并初始化数据库。错误: {str(e)}', 'error')
        return render_template('books/list.html',
                             books=[],
                             page=1,
                             total_pages=0,
                             keyword=keyword)

@bp.route('/<isbn>')
def book_detail(isbn):
    """图书详情页面"""
    book = execute_query(
        'SELECT * FROM book WHERE ISBN = %s',
        (isbn,), fetchone=True
    )

    if not book:
        flash('图书不存在', 'error')
        return redirect(url_for('books.book_list'))

    return render_template('books/detail.html', book=book)
