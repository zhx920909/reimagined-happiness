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
