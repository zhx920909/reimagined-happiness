from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

# 边提交边进行
with engine.connect() as conn:
    # 创建表
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS `users` (
      `id` int(11) PRIMARY KEY AUTO_INCREMENT,
      `username` varchar(255) NOT NULL,
      `password` varchar(255) NOT NULL
      )"""
    conn.execute(text(create_table_sql))

    # 插入数据
    conn.execute(text('INSERT INTO `users` (`username`, `password`) VALUES (:username, :password)'),
                 [{'username': 'admin', 'password': 'admin'}, {'username': 'user', 'password': 'user'}])
    conn.commit()

    # 查询数据
    result = conn.execute(text('SELECT * FROM `users`'))
    for row in result:
        print(row.username, row.password)

# 一次性开始
with engine.begin() as conn:
    # 更新数据
    conn.execute(text('UPDATE `users` SET `password` = :password WHERE `username` = :username'),
                 {'username': 'admin', 'password': 'admin123'})
