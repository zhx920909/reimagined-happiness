from sqlalchemy import create_engine

from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:root@localhost:3306/sims')

conn = engine.connect()


def create_table():
    sql = """
    create table if not exists `student`(
    `id` int auto_increment primary key,
    `stu_no` varchar(20) not null unique,
    `stu_name` varchar(20) not null,
    `stu_age` int not null,
    `stu_gender` varchar(20) not null
    )
    """
    conn.execute(text(sql))


# 欢迎界面


def welcome():
    print('*' * 25)
    print('欢迎进入学生信息管理系统')


# 用户菜单引导
def choose():
    while True:
        print('*' * 25)

        if not query_all_stu():
            print('当前学生列表为空，可进行如下操作')

            print('1. 添加学生信息')
            print('5. 退出系统')

            choice = input('请输入您的选择：')

            match choice:
                case '1':
                    add_menu()
                case '5':
                    exit()
                case _:
                    print('输入有误，请重新输入')
        else:
            print('您可进行如下操作')
            print('1. 添加学生信息')
            print('2. 删除学生信息')
            print('3. 修改学生信息')
            print('4. 查询学生信息')
            print('5. 退出系统')

            choice = input('请输入您的选择：')

            match choice:
                case '1':
                    add_menu()
                case '2':
                    delete_choose()
                    pass
                case '3':
                    modify_choose()
                case '4':
                    query_choose()
                case '5':
                    exit()
                case _:
                    print('输入有误，请重新输入')


# 添加引导
def add_menu():
    while True:
        if add_stu():
            break
        else:
            print('*' * 25)


# 删除引导
def delete_choose():
    while True:
        delete_menu = input('请输入要执行的删除操作（[O]NE | [A]LL | [C]ANCEL）：')
        if delete_menu.upper() == 'O':
            delete_stu()
            break
        elif delete_menu.upper() == 'A':
            delete_all_stu()
            break
        elif delete_menu.upper() == 'C':
            print('取消删除')
            break
        else:
            print('输入有误，请重新输入')


# 修改引导
def modify_choose():
    while True:
        if modify_stu():
            break
        else:
            print('*' * 25)


# 查询引导
def query_choose():
    while True:
        query_menu = input('请输入要执行的查询操作（[O]NE | [A]LL | [C]ANCEL）：')
        if query_menu.upper() == 'O':
            stu_no = input('请输入要查询的学生学号：')
            student = query_stu(stu_no)
            if student:
                print(student)
            else:
                print('没有找到对应的学生')
            break
        elif query_menu.upper() == 'A':
            student_list = query_all_stu()
            for student in student_list:
                print(student)
            break
        elif query_menu.upper() == 'C':
            print('取消查询')
            break
        else:
            print('输入有误，请重新输入')


# 添加学生信息
def add_stu():
    stu_no = input('请输入学生学号：')

    if query_stu(stu_no):
        print('该学号已存在，请重新输入')
        return False

    stu_name = input('请输入学生姓名：')

    stu_age = input('请输入学生年龄：')

    if not stu_age.isdigit():
        print('学号必须是数字')
        return False

    stu_gender = input('请输入学生性别：')

    sql = text('insert into `student` (`stu_no`, `stu_name`, `stu_age`, `stu_gender`) values (:stu_no, :stu_name, :stu_age, :stu_gender)')
    result = conn.execute(sql, [{'stu_no': stu_no, 'stu_name': stu_name, 'stu_age': stu_age, 'stu_gender': stu_gender}])
    """
    rowcount 主要用于报告 UPDATE 或 DELETE 语句中匹配的行数。
    对于其他类型的语句（如 INSERT 和 SELECT），某些数据库API（DBAPI）可能不支持或提供有意义的 rowcount 值。
    因此，在使用 rowcount 时，可能会遇到警告或不确定的行为。
    对于 INSERT 语句，可以使用 lastrowid 来确认插入操作是否成功。这个属性通常更可靠，因为它直接返回插入行的主键值，但是需要确定的是，主键必须设置为 auto_increment。
    """
    if result.lastrowid:
        conn.commit()
        print(f'增加学生 {stu_name} 成功')
        return True
    else:
        conn.rollback()
        print(f'增加学生 {stu_name} 失败')
        return False


# 删除单个学生信息
def delete_stu():
    stu_no = input('请输入要删除的学生学号：')

    student = query_stu(stu_no)

    if not student:
        print('没有找到对应的学生，无法删除')
        return
    else:
        stu_name = student[2]
        sql = text('delete from `student` where `stu_no` = :stu_no')
        result = conn.execute(sql, [{'stu_no': stu_no}])
        if result.rowcount:
            conn.commit()
            print(f'删除 {stu_name} 成功')
        else:
            conn.rollback()
            print(f'删除 {stu_name} 失败')


# 删除所有学生信息
def delete_all_stu():
    sql = text('delete from `student`')
    result = conn.execute(sql)
    if result.rowcount:
        conn.commit()
        print('删除成功')
    else:
        conn.rollback()
        print('删除失败')


# 修改学生信息
def modify_stu():
    stu_no = input('请输入要修改的学生学号：')

    student = query_stu(stu_no)

    if not student:
        print('没有找到对应的学生，无法修改')
        return False
    else:
        stu_name_temp = student[2]
        stu_age_temp = student[3]
        stu_gender_temp = student[4]

        stu_name = input('请输入学生姓名：')
        stu_age = input('请输入学生年龄：')
        if not stu_age.isdigit():
            print('学号必须是数字')
            return False
        stu_gender = input('请输入学生性别：')
        if stu_name == stu_name_temp and int(stu_age) == stu_age_temp and stu_gender == stu_gender_temp:
            print('没有修改任何信息')
        else:
            sql = text('update `student` set `stu_name` = :stu_name, `stu_age` = :stu_age, `stu_gender` = :stu_gender where `stu_no` = :stu_no')
            result = conn.execute(sql, [{'stu_no': stu_no, 'stu_name': stu_name, 'stu_age': stu_age, 'stu_gender': stu_gender}])
            if result.rowcount:
                conn.commit()
                print('修改成功')
                if stu_name != stu_name_temp:
                    print(f'\t{stu_name_temp} 到 {stu_name}')
                if int(stu_age) != stu_age_temp:
                    print(f'\t{stu_age_temp} 到 {stu_age}')
                if stu_gender != stu_gender_temp:
                    print(f'\t{stu_gender_temp} 到 {stu_gender}')
                return True
            else:
                conn.rollback()
                print('修改失败')
                return False


# 根据学号查询学生信息
def query_stu(stu_no):
    sql = text('select * from `student` where stu_no = :stu_no')
    result = conn.execute(sql, {'stu_no': stu_no})
    row = result.fetchone()
    return row


# 查询所有学生信息
def query_all_stu():
    # 查询语句
    sql = text('select * from `student`')
    # 获取结果集
    result = conn.execute(sql)
    # 遍历结果集
    rows = result.fetchall()
    # 返回元组列表
    return rows


if __name__ == '__main__':
    create_table()
    welcome()
    choose()
