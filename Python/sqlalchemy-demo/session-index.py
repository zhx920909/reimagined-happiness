from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/demo')

select_statement = text('SELECT * FROM `users` where `username` = :username')
with Session(engine) as session:
    result = session.execute(select_statement, {'username': 'admin'})
    for row in result:
        print(row)

    session.execute(text('INSERT INTO `users` (`username`, `password`) VALUES (:username, :password)'),
                    {'username': 'hi', 'password': 'hi'})
    session.commit()
