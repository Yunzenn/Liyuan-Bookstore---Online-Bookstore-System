# 梨园书屋 - 网上书店系统

## 项目简介

这是一个基于 Flask + MySQL 的网上书店系统，实现了客户注册、图书浏览、订单管理等核心功能。前端采用 Aceternity UI 风格设计，具有现代化的视觉效果。

## 技术栈

- **后端**: Python 3.10+ + Flask
- **数据库**: MySQL 8.0
- **前端**: HTML + CSS + JavaScript (Aceternity UI 风格)
- **驱动**: PyMySQL

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `app/config.py` 文件，修改数据库连接信息：

```python
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'  # 修改为你的MySQL密码
MYSQL_DB = 'online_bookstore'
```

### 3. 初始化数据库

```bash
# 登录MySQL并执行建表脚本
mysql -u root -p < sql/create_tables.sql

# 插入测试数据
mysql -u root -p online_bookstore < sql/init_data.sql

# 创建视图（可选）
mysql -u root -p online_bookstore < sql/views.sql
```

### 4. 运行应用

```bash
python run.py
```

访问 http://localhost:5000 即可使用系统。

## 功能特性

### 客户管理
- ✅ 客户注册（唯一标识自动分配）
- ✅ 客户登录/登出
- ✅ 个人信息查看/修改

### 图书管理
- ✅ 图书目录浏览（Bento Grid 布局）
- ✅ 图书搜索（按书名、作者、ISBN）
- ✅ 图书详情查看

### 订单管理
- ✅ 创建订单（支持多图书）
- ✅ 订单列表查看
- ✅ 订单详情查看
- ✅ 订单状态管理（待付款→已付款→已发货→已完成）
- ✅ 订单取消（自动恢复库存）

## 项目结构

```
数据库实验/
├── 需求.md                  # 需求文档
├── 开发文档.md              # 开发文档
├── 规范文档.md              # 编码规范
├── 需求对照表.md            # 需求-实现对照
├── README.md                # 本文件
├── design/                  # 设计文档
│   ├── 数据流图.md
│   ├── 数据字典.md
│   ├── ER图.md
│   └── 逻辑设计.md
├── sql/                     # SQL脚本
│   ├── create_tables.sql    # 建表语句
│   ├── init_data.sql        # 测试数据
│   └── views.sql            # 视图定义
├── app/                     # Flask应用
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── routes/
│   │   ├── auth.py          # 认证路由
│   │   ├── books.py         # 图书路由
│   │   └── orders.py        # 订单路由
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── books/
│   │   └── orders/
│   └── static/
│       ├── css/style.css    # Aceternity UI 风格样式
│       └── js/main.js       # 交互效果
├── requirements.txt
└── run.py
```

## 测试账号

系统预置了以下测试账号（密码统一为 `123456`）：

| 邮箱 | 姓名 |
|------|------|
| zhangsan@example.com | 张三 |
| lisi@example.com | 李四 |
| wangwu@example.com | 王五 |

## 订单状态流转

```
待付款 ──付款──▶ 已付款 ──发货──▶ 已发货 ──确认──▶ 已完成
   │                                              │
   └────────────────取消──────────────────────────┘
```

## 设计亮点

1. **Aceternity UI 风格**: 毛玻璃效果、渐变背景、卡片悬停发光动画
2. **Bento Grid 布局**: 现代化的图书展示网格
3. **浮动导航栏**: 滚动时自动调整样式
4. **订单状态可视化**: 清晰的状态标签和流转说明
5. **响应式设计**: 适配不同屏幕尺寸
