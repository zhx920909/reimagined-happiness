# SQLAlchemy

## 概述

> 官网：https://docs.sqlalchemy.org/en/20/

> 中文参考：https://github.com/OpenDocCN/py-docs-zh/blob/master/docs/sqlalch_20/sqlalch20_001.md

![SQLAlchemy Components](pic/SQLAlchemy Components.png)

SQLAlchemy 包括以下组件：
ORM（对象关系映射）
Core（核心）

SQLAlchemy Core 中最突出的部分是 SQL 表达式语言。

## 使用

### 安装

```shell
pip install sqlalchemy
```

```shell
conda install sqlalchemy
```

### 验证（检查 SQLAlchemy 版本）

```python
import sqlalchemy

print(sqlalchemy.__version__)
```

### 建立连接

每一个连接到数据库的 SQLAlchemy 应用程序都需要使用一个 `Engine`。
该引擎通常是一个全局对象，仅为特定数据库服务器创建一次，并且使用 URL 字符串进行配置，该字符串将描述它应该如何连接到数据库主机或后端。

PyMySQL

> https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql

Connecting String:

```
mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
```

`mysql+pymysql` 是一个 URL 前缀，它告诉 SQLAlchemy 正在与 MySQL 数据库进行通信，并且使用 PyMySQL
作为用来与特定数据库交互的第三方驱动程序（DBAPI）。

`<username>:<password>@<host>/<dbname>[?<options>]` 是一个 URL
的基本格式，其中 `<username>` 和 `<password>` 是数据库用户名和密码，`<host>` 是数据库主机地址，`<dbname>` 是数据库名，

```python
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')
```

### 处理事务和 DBAPI

分为两种方式：一种是 Connection 模式，一种是 Session 模式。

#### Connection 模式

##### 获取连接

与数据库的所有交互都是通过 Connection 对象完成的

```python
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

with engine.connect() as conn:  # 提供称为 Connection 的数据库连接单元
    pass
```

##### DDL、DML

文本 SQL 使用一个叫做 text() 的构造发出

###### 查询

返回一个 Result 对象

```python
from sqlalchemy import create_engine

from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

with engine.connect() as conn:
    result = conn.execute(text('select * from `users`'))
    for row in result:
        print(row)
```

TODO: Result 对象

返回的对象被称为 Result 结果行的可迭代对象。对象 Row 本身的作用类似于 Python 命名元组。

###### 增删改

1. 边提交边进行

需要调用 `Connection.commit()` 方法来提交事务，在块内调用此方法后，我们可以继续运行更多的 SQL
语句，如果必要的话，我们可以再次调用 `Connection.commit()` 来进行后续语句的提交。SQLAlchemy 将这种风格称为 **边提交边进行
**。

```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

with engine.connect() as conn:
    """插入数据"""
    conn.execute(text('INSERT INTO `users` (`username`, `password`) VALUES (:username, :password)'),
                 [{'username': 'admin', 'password': 'admin'}, {'username': 'user', 'password': 'user'}])
    conn.commit()

    """修改数据"""
    conn.execute(text('UPDATE `users` SET `password` = :password WHERE `username` = :username'),
                 {'username': 'admin', 'password': 'admin123'})
    conn.commit()
```

2. 一次性开始

另一种提交数据的风格，即我们可以事先将我们的 `connect` 块声明为事务块。在这种操作模式下，我们使用 `Engine.begin()`
方法来获取连接，而不是使用 `Engine.connect()` 方法。这种方法既管理了 Connection 的范围，也在块成功的情况下，在事务结束时包含了
commit，或者在块出现异常时回滚。这种风格被称为**一次性开始**

```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

with engine.begin() as conn:
    """插入数据"""
    conn.execute(text('INSERT INTO `users` (`username`, `password`) VALUES (:username, :password)'),
                 [{'username': 'admin', 'password': 'admin'}, {'username': 'user', 'password': 'user'}])
    # conn.commit()

    """修改数据"""
    conn.execute(text('UPDATE `users` SET `password` = :password WHERE `username` = :username'),
                 {'username': 'admin', 'password': 'admin123'})
    # conn.commit()
```

TODO: 绑定参数

#### Session 模式

当使用 ORM 时，与数据库交互的基本事务对象称为 Session，与 Connection 非常相似，实际上，当使用 Session 时，它会内部引用一个
Connection，然后使用它来发出 SQL。

直接将对 `with engine.connect() as conn` 的调用替换为 `with Session(engine) as session`
，然后像使用 `Connection.execute()` 方法一样使用 `Session.execute()` 方法。

像 Connection 一样，Session 也具有**边提交边执行**的行为，即使用 `Session.commit()` 方法