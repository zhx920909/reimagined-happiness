# SQLAlchemy

## 概述

> 官网：https://docs.sqlalchemy.org/en/20/

> 中文：https://github.com/OpenDocCN/py-docs-zh/blob/master/docs/sqlalch_20/sqlalch20_001.md

## 使用

- 安装

```shell
pip install sqlalchemy
```

- 验证

```python
import sqlalchemy

print(sqlalchemy.__version__)
```

- 建立连接

PyMySQL

> https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql

Connecting String:

```
mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
```

```python
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/test')
```

- 获取连接

```python
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/test')

with engine.connect() as conn:
    pass
```

- SQL 操作

文本 SQL 使用一个叫做 text() 的构造发出

```python
from sqlalchemy import create_engine

from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/test')

with engine.connect() as conn:
    conn.execute(text('select 1'))
```

- 使用 ORM 会话 session

当使用 ORM 时，与数据库交互的基本事务对象称为 Session，与 Connection 非常相似，实际上，当使用 Session 时，它会内部引用一个
Connection，然后使用它来发出 SQL。

直接将对 `with engine.connect() as conn` 的调用替换为 `with Session(engine) as session`
，然后像使用 `Connection.execute()` 方法一样使用 `Session.execute()` 方法。