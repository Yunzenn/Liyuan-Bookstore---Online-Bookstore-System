from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import execute_query, execute_insert

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """客户注册"""
    if request.method == 'POST':
        # 获取表单数据
        customer_name = request.form.get('customer_name', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # 验证必填字段
        if not customer_name or not email or not password:
            flash('请填写所有必填字段', 'error')
            return render_template('auth/register.html')

        # 验证密码一致性
        if password != confirm_password:
            flash('两次输入的密码不一致', 'error')
            return render_template('auth/register.html')

        # 验证邮箱是否已存在
        existing = execute_query(
            'SELECT customer_id FROM customer WHERE email = %s',
            (email,), fetchone=True
        )
        if existing:
            flash('该邮箱已被注册', 'error')
            return render_template('auth/register.html')

        # 生成密码哈希
        password_hash = generate_password_hash(password)

        # 插入新客户
        try:
            customer_id = execute_insert(
                'INSERT INTO customer (customer_name, address, phone, email, password_hash) VALUES (%s, %s, %s, %s, %s)',
                (customer_name, address, phone, email, password_hash)
            )
            flash('注册成功，请登录', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'注册失败: {str(e)}', 'error')
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """客户登录"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # 查询客户
        customer = execute_query(
            'SELECT * FROM customer WHERE email = %s',
            (email,), fetchone=True
        )

        # 验证密码
        if customer and check_password_hash(customer['password_hash'], password):
            # 登录成功，存储session
            session['customer_id'] = customer['customer_id']
            session['customer_name'] = customer['customer_name']
            flash('登录成功', 'success')
            return redirect(url_for('books.book_list'))
        else:
            flash('邮箱或密码错误', 'error')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """登出"""
    session.clear()
    flash('已成功登出', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/profile')
def profile():
    """个人信息"""
    if 'customer_id' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('auth.login'))

    customer = execute_query(
        'SELECT * FROM customer WHERE customer_id = %s',
        (session['customer_id'],), fetchone=True
    )
    return render_template('auth/profile.html', customer=customer)

@bp.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    """编辑个人信息"""
    if 'customer_id' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()

        if not customer_name:
            flash('客户名不能为空', 'error')
            return render_template('auth/profile_edit.html')

        try:
            execute_insert(
                'UPDATE customer SET customer_name = %s, address = %s, phone = %s WHERE customer_id = %s',
                (customer_name, address, phone, session['customer_id'])
            )
            session['customer_name'] = customer_name
            flash('个人信息更新成功', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            flash(f'更新失败: {str(e)}', 'error')

    customer = execute_query(
        'SELECT * FROM customer WHERE customer_id = %s',
        (session['customer_id'],), fetchone=True
    )
    return render_template('auth/profile_edit.html', customer=customer)
