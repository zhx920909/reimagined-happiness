class Student(object):
    def __init__(self, no, name, age, gender):
        self.__no = no
        self.__name = name
        self.__age = age
        self.__gender = gender

    def set_no(self, no, other):
        if other.get_no() == no:
            print('学号重复，请重新输入')
            return False
        else:
            self.__no = no
            return True

    def get_no(self):
        return self.__no

    def set_name(self, name):
        self.__name = name
        return True

    def get_name(self):
        return self.__name

    def set_age(self, age):
        if not age.isdigit():
            print('年龄必须是数字')
            return False
        else:
            self.__age = age
            return True

    def get_age(self):
        return self.__age

    def set_gender(self, gender):
        self.__gender = gender
        return True

    def get_gender(self):
        return self.__gender
