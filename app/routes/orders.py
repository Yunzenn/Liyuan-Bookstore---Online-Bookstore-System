from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from app.database import execute_query, execute_insert, execute_update

bp = Blueprint('orders', __name__, url_prefix='/orders')

def login_required(f):
    """登录验证装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
def order_list():
    """订单列表页面"""
    customer_id = session['customer_id']

    # 查询当前用户的所有订单
    orders = execute_query("""
        SELECT o.*,
               COUNT(oi.ISBN) as item_count
        FROM `order` o
        LEFT JOIN order_item oi ON o.order_id = oi.order_id
        WHERE o.customer_id = %s
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
    """, (customer_id,))

    return render_template('orders/list.html', orders=orders)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_order():
    """创建订单页面"""
    if request.method == 'POST':
        # 获取选中的图书和数量
        selected_books = []
        for key, value in request.form.items():
            if key.startswith('quantity_') and value and int(value) > 0:
                isbn = key.replace('quantity_', '')
                quantity = int(value)
                selected_books.append((isbn, quantity))

        if not selected_books:
            flash('请至少选择一本图书', 'error')
            return redirect(url_for('orders.create_order'))

        # 验证库存并计算总金额
        total_amount = 0
        order_items = []
        for isbn, quantity in selected_books:
            book = execute_query(
                'SELECT * FROM book WHERE ISBN = %s',
                (isbn,), fetchone=True
            )
            if not book:
                flash(f'图书 {isbn} 不存在', 'error')
                return redirect(url_for('orders.create_order'))

            if book['stock'] < quantity:
                flash(f'图书《{book["title"]}》库存不足，当前库存: {book["stock"]}', 'error')
                return redirect(url_for('orders.create_order'))

            subtotal = book['price'] * quantity
            total_amount += subtotal
            order_items.append({
                'isbn': isbn,
                'quantity': quantity,
                'unit_price': book['price'],
                'book': book
            })

        # 创建订单
        try:
            order_id = execute_insert(
                'INSERT INTO `order` (customer_id, total_amount) VALUES (%s, %s)',
                (session['customer_id'], total_amount)
            )

            # 插入订单明细
            for item in order_items:
                execute_insert(
                    'INSERT INTO order_item (order_id, ISBN, quantity, unit_price) VALUES (%s, %s, %s, %s)',
                    (order_id, item['isbn'], item['quantity'], item['unit_price'])
                )

                # 更新库存
                execute_update(
                    'UPDATE book SET stock = stock - %s WHERE ISBN = %s',
                    (item['quantity'], item['isbn'])
                )

            flash('订单创建成功', 'success')
            return redirect(url_for('orders.order_detail', order_id=order_id))

        except Exception as e:
            flash(f'订单创建失败: {str(e)}', 'error')
            return redirect(url_for('orders.create_order'))

    # GET请求：显示图书选择页面
    books = execute_query('SELECT * FROM book WHERE stock > 0 ORDER BY title')
    return render_template('orders/create.html', books=books)

@bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    """订单详情页面"""
    # 查询订单信息
    order = execute_query("""
        SELECT o.*, c.customer_name, c.email
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        WHERE o.order_id = %s
    """, (order_id,), fetchone=True)

    if not order:
        flash('订单不存在', 'error')
        return redirect(url_for('orders.order_list'))

    # 验证权限（只能查看自己的订单）
    if order['customer_id'] != session['customer_id']:
        flash('无权查看此订单', 'error')
        return redirect(url_for('orders.order_list'))

    # 查询订单明细
    items = execute_query("""
        SELECT oi.*, b.title, b.author, b.ISBN
        FROM order_item oi
        JOIN book b ON oi.ISBN = b.ISBN
        WHERE oi.order_id = %s
    """, (order_id,))

    return render_template('orders/detail.html', order=order, items=items)

@bp.route('/<int:order_id>/pay', methods=['POST'])
@login_required
def pay_order(order_id):
    """付款操作"""
    order = execute_query(
        'SELECT * FROM `order` WHERE order_id = %s AND customer_id = %s',
        (order_id, session['customer_id']), fetchone=True
    )

    if not order:
        flash('订单不存在', 'error')
        return redirect(url_for('orders.order_list'))

    if order['status'] != '待付款':
        flash('该订单状态无法付款', 'error')
        return redirect(url_for('orders.order_detail', order_id=order_id))

    try:
        execute_update(
            'UPDATE `order` SET status = %s WHERE order_id = %s',
            ('已付款', order_id)
        )
        flash('付款成功', 'success')
    except Exception as e:
        flash(f'付款失败: {str(e)}', 'error')

    return redirect(url_for('orders.order_detail', order_id=order_id))

@bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """取消订单"""
    order = execute_query(
        'SELECT * FROM `order` WHERE order_id = %s AND customer_id = %s',
        (order_id, session['customer_id']), fetchone=True
    )

    if not order:
        flash('订单不存在', 'error')
        return redirect(url_for('orders.order_list'))

    if order['status'] not in ['待付款', '已付款']:
        flash('该订单状态无法取消', 'error')
        return redirect(url_for('orders.order_detail', order_id=order_id))

    try:
        # 恢复库存
        items = execute_query(
            'SELECT * FROM order_item WHERE order_id = %s',
            (order_id,)
        )
        for item in items:
            execute_update(
                'UPDATE book SET stock = stock + %s WHERE ISBN = %s',
                (item['quantity'], item['ISBN'])
            )

        # 更新订单状态
        execute_update(
            'UPDATE `order` SET status = %s WHERE order_id = %s',
            ('已取消', order_id)
        )
        flash('订单已取消', 'success')
    except Exception as e:
        flash(f'取消失败: {str(e)}', 'error')

    return redirect(url_for('orders.order_detail', order_id=order_id))

@bp.route('/<int:order_id>/ship', methods=['POST'])
@login_required
def ship_order(order_id):
    """发货操作（管理员功能）"""
    order = execute_query(
        'SELECT * FROM `order` WHERE order_id = %s',
        (order_id,), fetchone=True
    )

    if not order:
        flash('订单不存在', 'error')
        return redirect(url_for('orders.order_list'))

    if order['status'] != '已付款':
        flash('该订单状态无法发货', 'error')
        return redirect(url_for('orders.order_detail', order_id=order_id))

    try:
        execute_update(
            'UPDATE `order` SET status = %s WHERE order_id = %s',
            ('已发货', order_id)
        )
        flash('发货成功', 'success')
    except Exception as e:
        flash(f'发货失败: {str(e)}', 'error')

    return redirect(url_for('orders.order_detail', order_id=order_id))

@bp.route('/<int:order_id>/complete', methods=['POST'])
@login_required
def complete_order(order_id):
    """完成订单（确认收货）"""
    order = execute_query(
        'SELECT * FROM `order` WHERE order_id = %s AND customer_id = %s',
        (order_id, session['customer_id']), fetchone=True
    )

    if not order:
        flash('订单不存在', 'error')
        return redirect(url_for('orders.order_list'))

    if order['status'] != '已发货':
        flash('该订单状态无法确认收货', 'error')
        return redirect(url_for('orders.order_detail', order_id=order_id))

    try:
        execute_update(
            'UPDATE `order` SET status = %s WHERE order_id = %s',
            ('已完成', order_id)
        )
        flash('订单已完成', 'success')
    except Exception as e:
        flash(f'操作失败: {str(e)}', 'error')

    return redirect(url_for('orders.order_detail', order_id=order_id))
