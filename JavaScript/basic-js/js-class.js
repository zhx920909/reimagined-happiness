class Student {
    constructor(stu_no, stu_name, stu_age, stu_gender) {
        this.stu_no = stu_no
        this.stu_name = stu_name
        this.stu_age = stu_age
        this.stu_gender = stu_gender
    }

    // 注意，和普通函数定义不一样
    introduce() {
        console.log(stu.stu_no)
        console.log(stu.stu_name)
        console.log(stu.stu_age)
        console.log(stu.stu_gender)
    }
}

let stu = new Student('1001', 'jackie', 17, 'male')
stu.introduce()