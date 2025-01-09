# 1. 导入 PyMySQL 库
import pymysql

# 1.1 导入异常类
from pymysql import MySQLError

# 2. 创建与数据库服务的连接对象
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='sims')

# 3. 通过连接对象创建游标对象
cur = conn.cursor()


# 4. 通过游标对象发送 SQL 语句到服务器

# 4.1 创建表
def create_table():
    sql = '''
        create table if not exists student(
            stu_no varchar(10) primary key,
            stu_name varchar(20) not null,
            stu_age int,
            stu_gender varchar(10)
        )
    '''
    cur.execute(sql)


# 5. 增删改查

# 5.1 添加学生信息
def add_stu():
    stu_no = input('请输入学生学号：')
    stu_name = input('请输入学生姓名：')
    stu_age = input('请输入学生年龄：')
    stu_gender = input('请输入学生性别：')

    sql = f'''
        insert into student(stu_no, stu_name, stu_age, stu_gender)
        values('{stu_no}', '{stu_name}', {stu_age}, '{stu_gender}')
    '''

    try:
        affected_row = cur.execute(sql)
        if affected_row == 1:
            print('插入学生成功')
        conn.commit()
    except MySQLError as e:
        print('插入学生失败', e)
        conn.rollback()


# 5.2 查询所有学生信息
def query_all_stu():
    sql = 'select * from student'
    cur.execute(sql)
    # 获取查询结果集
    result = cur.fetchall()
    for row in result:
        print(row)


# 5.3 查询单个学生信息
def query_stu(stu_no):
    sql = f'select * from student where stu_no = "{stu_no}"'
    cur.execute(sql)
    result = cur.fetchone()
    return result


# 5.4 按照学号修改学生信息
def modify_stu():
    stu_no = input('请输入要修改的学生学号：')
    result = query_stu(stu_no)
    if result:
        print(result)
        stu_name = input('请输入学生姓名：')
        stu_age = input('请输入学生年龄：')
        stu_gender = input('请输入学生性别：')
        sql = f'''
            update student
            set stu_name = '{stu_name}', stu_age = {stu_age}, stu_gender = '{stu_gender}'
            where stu_no = '{stu_no}'
        '''
        try:
            affected_row = cur.execute(sql)
            if affected_row == 1:
                print('修改学生信息成功')
            conn.commit()
        except MySQLError as e:
            print('修改学生信息失败', e)
            conn.rollback()
    else:
        print('没有查询到该学生信息，无法修改')


# 5.5 按照学号删除学生信息
def delete_stu():
    stu_no = input('请输入您要删除的学生的学号：')
    result = query_stu(stu_no)
    if result:
        sql = f'delete from student where stu_no = "{stu_no}"'
        try:
            affected_row = cur.execute(sql)
            if affected_row == 1:
                print('删除学生成功')
            conn.commit()
        except MySQLError as e:
            print('删除学生信息失败', e)
            conn.rollback()
    else:
        print('没有查询到该学生信息，无法删除')


# 5.6 删除所有学生信息
def delete_all_stu():
    sql = 'delete from student'
    try:
        affected_row = cur.execute(sql)
        if affected_row > 0:
            print('删除所有学生成功')
        conn.commit()
    except MySQLError as e:
        print('删除所有学生信息失败', e)
        conn.rollback()


def welcome():
    print('*' * 25)
    print('欢迎进入学生信息管理系统')


def menu():
    print('*' * 25)
    print('1. 添加学生信息')
    print('2. 删除学生信息')
    print('3. 删除所有学生信息')
    print('4. 修改学生信息')
    print('5. 查询学生信息')
    print('6. 查询所有学生信息')
    print('7. 退出系统')


def exit_system():
    cur.close()
    conn.close()
    print('欢迎下次使用该系统')
    exit()


def choose():
    menu()
    choice = input('请输入你的选择：')
    # 3.10 版本，match case 语句
    match choice:
        case '1':
            # print('添加学生信息')
            add_stu()
        case '2':
            # print('删除学生信息')
            delete_stu()
        case '3':
            # print('删除所有学生信息')
            delete_all_stu()
        case '4':
            # print('修改学生信息')
            modify_stu()
        case '5':
            # print('查询学生信息')
            stu_no = input('请输入要查询的学生学号：')
            if query_stu(stu_no):
                print(query_stu(stu_no))
            else:
                print('没有查询到该学生信息')
        case '6':
            # print('查询所有学生信息')
            query_all_stu()
        case '7':
            # print('退出系统')
            exit_system()
    default: (
        print('输入有误，请重新输入'))


def main():
    create_table()
    while True:
        choose()


if __name__ == '__main__':
    welcome()
    main()
