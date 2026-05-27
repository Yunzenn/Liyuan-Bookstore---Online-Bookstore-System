# E-R图设计

## 1. 实体与属性

### 1.1 客户实体 (Customer)

```
┌─────────────────────────┐
│         客户            │
│      (Customer)         │
├─────────────────────────┤
│ ● customer_id (PK)     │
│   customer_name         │
│   address               │
│   phone                 │
│   email (UK)            │
│   password_hash         │
│   created_at            │
│   updated_at            │
└─────────────────────────┘
```

**属性说明：**
- customer_id：客户唯一标识，主键
- customer_name：客户姓名，必填
- address：客户地址
- phone：联系电话
- email：电子邮箱，唯一约束
- password_hash：密码哈希值，必填
- created_at：注册时间
- updated_at：信息更新时间

### 1.2 图书实体 (Book)

```
┌─────────────────────────┐
│         图书            │
│        (Book)           │
├─────────────────────────┤
│ ● ISBN (PK)            │
│   title                 │
│   author                │
│   price                 │
│   publisher             │
│   publish_year          │
│   stock                 │
└─────────────────────────┘
```

**属性说明：**
- ISBN：国际标准书号，主键
- title：书名，必填
- author：作者，必填
- price：定价，必填
- publisher：出版社
- publish_year：出版年份
- stock：库存数量

### 1.3 订单实体 (Order)

```
┌─────────────────────────┐
│         订单            │
│        (Order)          │
├─────────────────────────┤
│ ● order_id (PK)        │
│   customer_id (FK)      │
│   order_date            │
│   status                │
│   total_amount          │
└─────────────────────────┘
```

**属性说明：**
- order_id：订单唯一标识，主键
- customer_id：下单客户ID，外键
- order_date：下单时间
- status：订单状态（待付款/已付款/已发货/已完成/已取消）
- total_amount：订单总额

### 1.4 订单明细实体 (OrderItem)

```
┌─────────────────────────┐
│       订单明细          │
│      (OrderItem)        │
├─────────────────────────┤
│ ● order_id (PK, FK)   │
│ ● ISBN (PK, FK)        │
│   quantity              │
│   unit_price            │
└─────────────────────────┘
```

**属性说明：**
- order_id：所属订单ID，联合主键，外键
- ISBN：图书ISBN，联合主键，外键
- quantity：购买数量
- unit_price：下单时单价（记录历史价格）

---

## 2. 实体关系图

### 2.1 完整E-R图

```
                    ┌─────────────┐
                    │    客户     │
                    │  (Customer) │
                    └──────┬──────┘
                           │
                           │ 1
                           │
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    图书     │    │    订单     │    │   订单明细   │
│   (Book)    │◄───│   (Order)   │───▶│ (OrderItem) │
└─────────────┘ N  └─────────────┘ 1  └─────────────┘
      ▲                                      
      │                                      
      │ M                                    
      │                                      
      └────────────────────────────────────────┘
                         N
```

### 2.2 关系说明

#### 关系1：客户-订单 (Customer-Order)
- **类型**：一对多 (1:N)
- **含义**：一个客户可以下多个订单，一个订单只属于一个客户
- **参与约束**：
  - 客户端：部分参与（客户可以不下订单）
  - 订单端：全部参与（订单必须有客户）
- **基数约束**：(0,N) - (1,1)

#### 关系2：订单-订单明细 (Order-OrderItem)
- **类型**：一对多 (1:N)
- **含义**：一个订单包含多个订单明细项
- **参与约束**：
  - 订单端：部分参与（订单可以没有明细？不，至少1项）
  - 明细端：全部参与
- **基数约束**：(1,N) - (1,1)

#### 关系3：图书-订单明细 (Book-OrderItem)
- **类型**：一对多 (1:N)
- **含义**：一种图书可以出现在多个订单明细中
- **参与约束**：
  - 图书端：部分参与（图书可以没有被订购）
  - 明细端：全部参与
- **基数约束**：(0,N) - (1,1)

---

## 3. 扩展E-R图（含弱实体）

### 3.1 订单明细作为弱实体

订单明细是依赖于订单存在的弱实体：

```
        ┌─────────────┐
        │    订单     │       ┌─────────────┐
        │   (Order)   │       │    图书     │
        │  强实体     │       │   (Book)    │
        └──────┬──────┘       │   强实体    │
               │              └──────┬──────┘
               │ 1                   │ 1
               │                     │
               ▼                     ▼
        ┌─────────────────────────────────────┐
        │            订单明细                  │
        │          (OrderItem)                │
        │           弱实体                    │
        │     (依赖于Order和Book)             │
        └─────────────────────────────────────┘
```

**说明：**
- 订单明细的存在依赖于订单的存在
- 如果订单被删除，其所有明细也应被删除
- 这体现了**存在依赖**和**标识依赖**

---

## 4. 属性类型分类

### 4.1 简单属性与复合属性
| 实体 | 简单属性 | 复合属性 |
|------|---------|---------|
| 客户 | customer_id, customer_name, phone, email, created_at, updated_at | address (省+市+区+详细地址) |
| 图书 | ISBN, title, author, price, publisher, publish_year, stock | - |
| 订单 | order_id, order_date, status, total_amount | - |
| 订单明细 | quantity, unit_price | - |

### 4.2 单值属性与多值属性
- 所有属性均为单值属性
- 如需存储多个电话或地址，可设计为多值属性或新建关联表

### 4.3 派生属性
| 派生属性 | 来源 | 计算方式 |
|----------|------|---------|
| 订单总额 (total_amount) | 订单明细 | SUM(quantity × unit_price) |
| 库存状态 | stock | stock > 0 ? "有货" : "缺货" |

---

## 5. 参与约束与基数约束汇总

| 关系 | 实体1 | 实体2 | 基数 | 参与约束 |
|------|-------|-------|------|---------|
| 下单 | Customer | Order | 1:N | 客户(0,N) - 订单(1,1) |
| 包含 | Order | OrderItem | 1:N | 订单(1,N) - 明细(1,1) |
| 属于 | Book | OrderItem | 1:N | 图书(0,N) - 明细(1,1) |

---

## 6. 将E-R图转换为关系模式

### 6.1 转换规则

1. **实体转换**：每个实体转换为一个关系模式
2. **1:N关系**：将"1"端的主键加入"N"端作为外键
3. **M:N关系**：新建关系模式，包含两端主键
4. **弱实体**：转换时需包含所依赖强实体的主键

### 6.2 转换结果

#### 客户关系模式
```
Customer(
    customer_id     INT PRIMARY KEY,
    customer_name   VARCHAR(50) NOT NULL,
    address         VARCHAR(200),
    phone           VARCHAR(20),
    email           VARCHAR(100) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    created_at      DATETIME,
    updated_at      DATETIME
)
```

#### 图书关系模式
```
Book(
    ISBN            VARCHAR(13) PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    author          VARCHAR(100) NOT NULL,
    price           DECIMAL(10,2) NOT NULL,
    publisher       VARCHAR(100),
    publish_year    YEAR,
    stock           INT DEFAULT 0
)
```

#### 订单关系模式
```
Order(
    order_id        INT PRIMARY KEY,
    customer_id     INT NOT NULL,
    order_date      DATETIME NOT NULL,
    status          VARCHAR(20) DEFAULT '待付款',
    total_amount    DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
)
```

#### 订单明细关系模式
```
OrderItem(
    order_id        INT,
    ISBN            VARCHAR(13),
    quantity        INT NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, ISBN),
    FOREIGN KEY (order_id) REFERENCES Order(order_id),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
)
```

---

## 7. 范式判断

### 7.1 各表范式分析

| 表名 | 主键 | 范式级别 | 说明 |
|------|------|---------|------|
| Customer | customer_id | **BCNF** | 所有属性完全依赖于主键，无传递依赖 |
| Book | ISBN | **BCNF** | 所有属性完全依赖于主键，无传递依赖 |
| Order | order_id | **BCNF** | 所有属性完全依赖于主键，无传递依赖 |
| OrderItem | (order_id, ISBN) | **BCNF** | 所有属性完全依赖于联合主键 |

### 7.2 范式验证

**Customer表：**
- 1NF：✓ 所有属性原子性
- 2NF：✓ 单属性主键，不存在部分依赖
- 3NF：✓ 无传递依赖（如 city→zip_code 不存在）
- BCNF：✓ 所有决定因素都是候选键

**Book表：**
- 1NF：✓ 所有属性原子性
- 2NF：✓ 单属性主键
- 3NF：✓ 无传递依赖
- BCNF：✓

**Order表：**
- 1NF：✓
- 2NF：✓
- 3NF：✓
- BCNF：✓

**OrderItem表：**
- 1NF：✓
- 2NF：✓ quantity和unit_price都完全依赖于(order_id, ISBN)
- 3NF：✓ 无传递依赖
- BCNF：✓
