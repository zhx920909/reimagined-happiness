from student import Student

student_list = []


# 欢迎界面
def welcome():
    print('*' * 25)
    print('欢迎进入学生信息管理系统')


# 用户菜单引导
def choose():
    while True:
        print('*' * 25)

        if not student_list:
            print('当前学生列表为空，可进行如下操作')

            print('1. 添加学生信息')
            print('5. 退出系统')

            choice = input('请输入您的选择：')

            match choice:
                case '1':
                    add_menu()
                case '5':
                    exit_sys()
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
                case '3':
                    modify_choose()
                case '4':
                    query_choose()
                case '5':
                    exit_sys()
                case _:
                    print('输入有误，请重新输入')


# 退出系统
def exit_sys():
    confirm = input('确认退出？[Y/N]：')
    if confirm.upper() == 'Y':
        exit()
    else:
        print('取消退出')


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
            student_list_t = query_stu(stu_no)
            if student_list_t:
                (student,) = student_list_t
                print(f'{student.get_no()}\t{student.get_name()}\t{student.get_age()}\t{student.get_gender()}')
            else:
                print('没有找到对应的学生')
            break
        elif query_menu.upper() == 'A':
            query_all_stu()
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

    student_info = Student(stu_no, stu_name, stu_age, stu_gender)

    student_list.append(student_info)

    print(f'增加学生 {stu_name} 成功')

    return True


# 删除单个学生信息
def delete_stu():
    stu_no = input('请输入要删除的学生学号：')

    student_list_t = query_stu(stu_no)

    if not student_list_t:
        print('没有找到对应的学生，无法删除')
        return
    else:
        confirm = input('确认删除？[Y/N]：')
        if confirm.upper() == 'Y':
            # 修改列表的原始值，通过切片的方式来做
            student_list[::] = (student for student in student_list if student.get_no() != stu_no)

            (student,) = student_list_t
            print(f'删除 {student.get_name()} 成功')
        else:
            print('取消删除')
            return


# 删除所有学生信息
def delete_all_stu():
    student_list.clear()
    print('删除成功')


# 修改学生信息
def modify_stu():
    stu_no = input('请输入要修改的学生学号：')

    student_list_t = query_stu(stu_no)

    if not student_list_t:
        print('没有找到对应的学生，无法修改')
        return False
    else:
        confirm = input('确认修改？[Y/N]：')
        if confirm.upper() == 'Y':
            for student in student_list:
                if student.get_no() == stu_no:
                    stu_name_t = student.get_name()
                    stu_age_t = student.get_age()
                    stu_gender_t = student.get_gender()

                    stu_name = input('请输入学生姓名：')
                    stu_age = input('请输入学生年龄：')
                    if not stu_age.isdigit():
                        print('学号必须是数字')
                        return False
                    stu_gender = input('请输入学生性别：')

                    student.set_name(stu_name)
                    student.set_age(stu_age)
                    student.set_gender(stu_gender)

                    if stu_name == stu_name_t and int(stu_age) == stu_age_t and stu_gender == stu_gender_t:
                        print('没有修改任何信息')
                    else:
                        print('修改成功')

                        if stu_name != stu_name_t:
                            print(f'\t{stu_name_t} 到 {stu_name}')
                        if int(stu_age) != stu_age_t:
                            print(f'\t{stu_age_t} 到 {stu_age}')
                        if stu_gender != stu_gender_t:
                            print(f'\t{stu_gender_t} 到 {stu_gender}')

                    break
            return True
        else:
            print('取消修改')
            return False


# 查询学生信息
def query_stu(stu_no):
    return tuple(student for student in student_list if student.get_no() == stu_no)


# 查询所有学生信息
def query_all_stu():
    for student in student_list:
        print(f'{student.get_no()}\t{student.get_name()}\t{student.get_age()}\t{student.get_gender()}')


if __name__ == '__main__':
    welcome()
    choose()
