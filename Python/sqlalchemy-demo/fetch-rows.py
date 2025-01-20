from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

# ResultProxy
with engine.connect() as conn:
    # 查询数据
    result = conn.execute(text('SELECT * FROM `users`'))

    # 1. 直接输出 Result 对象
    # print(result)  # <sqlalchemy.engine.cursor.CursorResult object at 0x000001A76BC3D320>

    # 2. 遍历结果集的第一行
    # row = result.fetchone()
    # print(row)  # (1, 'admin', 'admin123')

    # 3. 遍历结果集的所有行
    # rows = result.fetchall()  #
    # for row in rows:
    #     print(row)
    #     # (1, 'admin', 'admin123')
    #     # (2, 'user', 'user123')

    # 4. 直接遍历 Result 对象
    # for row in result:
    #     print(row)
    #     # (1, 'admin', 'admin123')
    #     # (2, 'user', 'user123')

    # 5. 输出 Result 对象的首行
    # print(result.first())  # (1, 'admin', 'admin123')

    # 6. 输出 Result 对象的所有行
    # print(result.all())  # [(1, 'admin', 'admin123'), (2, 'user', 'user123')]

    # 7. 多种方式解析 Result 对象
    # 7.1 元组表达式
    # for _, username, password in result:
    #     print(_, username, password)
    #     # 1 admin admin123
    #     # 2 user user123

    # 7.2 整数索引
    # for row in result:
    #     print(row[0], row[1], row[2])
    #     # 1 admin admin123
    #     # 2 user user123

    # 7.3 属性名称
    # for row in result:
    #     print(row.id, row.username, row.password)
    #     # 1 admin admin123
    #     # 2 user user123

    # 7.4 映射
    # for dict_row in result.mappings():  # 为了确保 dict_row 是一个字典类型
    #     print(dict_row['id'], dict_row['username'], dict_row['password'])
    #     # 1 admin admin123
    #     # 2 user user123
