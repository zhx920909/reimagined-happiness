# Python Guide For Myself

>   参考书籍：[The Hitchhiker’s Guide to Python](https://docs.python-guide.org/)

## Development Environment

### Python Interpreter

Of course Python 3.x，Python 官网 [Python](https://www.python.org/)

### Python Platform

但是一般情况下不会采用 Python 解释器的方案，虽然可以通过虚拟环境的方式解决包管理和环境独立的问题，但是环境版本无法切换。

-   Anaconda 官网 [Anaconda](https://www.anaconda.com/)

-   Miniconda 官网 [Miniconda](https://docs.anaconda.com/miniconda/)

#### Differences

Both the Anaconda Distribution and Miniconda installers include the conda package and environment manager.

Miniconda is a free, miniature installation of Anaconda Distribution that includes only conda, Python, the packages they both depend on, and a small number of other useful packages. But Anaconda Distribution contains over 300 automatically-installed packages that work well together out of the box.

If you know exactly what packages you want to use and you don’t want a large download, use Miniconda.

### Python Environment

PyCharm 默认推荐如下：

-   Virtualenv
-   Conda

## Structuring Project

### Package and Module

Packages include Modules.

任意包含 \_\_init\_\_.py 文件的目录都被认为是一个 Python 包，当然使用 PyCharm 在项目上右键新建 Python Package 的时候，会自动创建空白的 \_\_init\_\_.py。

简单理解，一个 .py 文件就是一个 Module。

使用 `tree` 命令生成的 tutorial 项目的树形结构如下：

```
tutorial
│
│  test.py
│
├─package1
│  │  module1.py
│  │  module2.py
│  │  __init__.py
│
└─package2
    │  module1.py
    │  __init__.py
```

其中的代码文件如下所示：

```python
# package1
# module1.py

def foo():
    return "hello foo"

```

```python
# package1
# module2.py

def bar():
    return "hello bar"

```

```python
# package2
# module1.py

def qux():
    return "hello qux"

```

```python
# test.py

import package1.module1 as p1m1
import package1.module2 as p1m2
from package2 import module1 as p2m1

print(p1m1.foo())
print(p1m2.bar())
print(p2m1.qux())

```

另外，如果需要导入模块中的函数进行使用，最好的做法是导入到模块，而不是直接导入函数。

```python
# bad

from modu import *

# good

from modu import func

# best

import modu
```

如下示例：

```python
# bad

from modu import *
x = sqrt(4)  # sqrt 是模块 modu 的一部分么？或是内建函数么？上文定义了么？

# good

from modu import sqrt
...
x = sqrt(4)  # 如果在 import 语句与这条语句之间，sqrt 没有被重复定义，它也许是模块 modu 的一部分

# best

import modu
x = modu.sqrt(4)  # sqrt 显然是属于模块 modu 的
```

### Decorator

在学习装饰器前，可以先过一遍函数。

#### 将函数赋值给变量

```python
def hi(nickname="joker"):
    return "hi, " + nickname


hello = hi  # 注意没有使用小括号，因为并不是在调用 hi 函数，而是在将它赋值给 greet 变量

print(hello())  # hi, joker

del hi

# print(hi())  # NameError: name 'hi' is not defined

print(hello())  # hi, joker

```

#### 在函数中定义函数

```python
def hi(nickname="joker"):
    print("now you are inside-before the hi() function")

    def greet():
        return "now you are in the greet() function"

    def welcome():
        return "now you are in the welcome() function"

    print(greet())
    print(welcome())

    print("now you are inside-after in the hi() function")


hi()
# now you are inside-before the hi() function
# now you are in the greet() function
# now you are in the welcome() function
# now you are inside-after in the hi() function

# 无论何时调用 hi()，greet() 和 welcome() 将会同时被调用

# greet() 和 welcome() 函数在 hi() 函数之外是不能访问的
greet()
# NameError: name 'greet' is not defined

```

#### 从函数中返回函数

```python
def hi(nickname="joker"):
    def greet():
        return "now you are in the greet() function"

    def welcome():
        return "now you are in the welcome() function"

    if nickname == "joker":
        return greet
    else:
        return welcome


hello = hi()
print(hello)
# <function hi.<locals>.greet at 0x000001CADC3211E0>

# 表示 hello 变量现在指向到 hi() 函数中的 greet() 函数

print(hello())
# now you are in the greet() function

```

#### 将函数作为参数传给另一个函数

```python
def hi():
    return "hi joker!"


# 装饰器本质就是一个函数
def do_something_before_hi(func):
    print("I am doing some boring work before executing hi()")
    print(func())


do_something_before_hi(hi)
# I am doing some boring work before executing hi()
# hi joker!

```

引出装饰器：

装饰器（Decorators）本质上是一个函数，它可以接收一个函数作为参数并返回一个新的函数，允许在不修改原有函数代码的情况下，给原函数增加新的功能，这个新函数是对原函数的包装或增强。

#### 第一个装饰器

```python
def a_new_decorator(a_func):
    def wrap_the_function():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrap_the_function


def a_function_requiring_decoration():
    print("I am the function which needs some decoration to enhance my features")


a_function_requiring_decoration()
# I am the function which needs some decoration to enhance my features

# 装饰器（a_new_decorator）封装一个函数（a_function_requiring_decoration），并且用这样或者那样的方式来修改它的行为
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

a_function_requiring_decoration()
# I am doing some boring work before executing a_func()
# I am the function which needs some decoration to enhance my features
# I am doing some boring work after executing a_func()
```

##### `@` 语法糖

```python
def a_new_decorator(a_func):
    def wrap_the_function():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrap_the_function


"""
the @a_new_decorator is just a short way of saying:
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
"""


@a_new_decorator
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to enhance my features")


a_function_requiring_decoration()

```

##### 局限性：如何保留原函数信息

```python
def a_new_decorator(a_func):
    def wrap_the_function():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrap_the_function


@a_new_decorator
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to enhance my features")


# a_function_requiring_decoration()

print(a_function_requiring_decoration.__name__)
# 本意是输出 a_function_requiring_decoration
# 但此时输出 wrap_the_function
# 可以看出调用 a_function_requiring_decoration 函数时，实际上调用的是 wrap_the_function 函数
# 表示 a_function_requiring_decoration 函数被 wrap_the_function 替代了，它重写了 a_function_requiring_decoration 函数的名字和注释文档（docstring）
```

###### 解决

通过 `functools.wraps` 函数可以解决。

```python
from functools import wraps


def a_new_decorator(a_func):
    #  `@wraps` 接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。这可以让我们在装饰器里面访问在装饰之前的函数的属性
    @wraps(a_func)
    def wrap_the_function():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrap_the_function


@a_new_decorator
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to enhance my features")


print(a_function_requiring_decoration.__name__)
# a_function_requiring_decoration

```

#### 装饰器步骤

```python
from functools import wraps


# 1. 定义装饰器，接收一个函数作为参数
def decorator(func):
    @wraps(func)
    # 2. 定义包装函数，调用原函数，并可以在调用前后添加额外的逻辑
    def wrapper():
        print("before calling ...")
        func()
        print("after calling ...")

    # 3. 返回包装函数，注意是返回函数名，不能加小括号，否则就变成了返回函数调用结果了
    return wrapper


# 4. 使用 @ 语法，在需要被装饰的函数顶以前使用 @ 符号加上装饰器名称，Python 解释器会自动将该函数作为参数传递给装饰器，并将返回的新函数（包装函数）赋值给原函数名
@decorator
def hi():
    print("hi, joker")


hi()

```

#### 带参数的装饰器

```python
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("function is called with arguments: ", args, kwargs)
        result = func(*args, **kwargs)
        return result

    return wrapper


@decorator
def addition(n1, n2):
    return n1 + n2


@decorator
def hi(nickname):
    return "hi " + nickname


print(addition(8, 17))
# function is called with arguments:  (8, 17) {}
# 25

print(hi("joker"))
# function is called with arguments:  ('joker',) {}
# hi joker

```

#### 给装饰器带参数

使用一个外层函数来封装装饰器，该外层函数为新装饰器名称。

```python
from functools import wraps


def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(3)
def hi(nickname):
    print("hi " + nickname)


hi("joker")

```

### Context Manager

上下文管理器是一个 Python 对象，为操作提供了额外的上下文信息。 这种额外的信息， 在使用 with 语句初始化上下文，以及完成 with 块中的所有代码时，采用可调用的形式。

经典的示例，打开文件：

```python
# 以这种形式调用 open 能确保 f 的 close 函数会在某个时候被调用，减少开发人员的认知负担，并使代码更容易阅读
with open("file.txt", "r") as f:
    print(f.read())

```

##### 使用类实现

```python
class CustomOpen():
    # 首先实例化
    def __init__(self, filename):
        self.file = open(filename)

    # 调用 __enter__ 函数的返回值会在 as f 语句中被赋值给 f
    def __enter__(self):
        return self.file

    # 当 with 语句块中的内容执行完之后，会调用 __exit__ 函数
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


with CustomOpen("file.txt") as f:
    print(f.read())

```

##### 使用生成器方式实现

```python
from contextlib import contextmanager


@contextmanager
def custom_open(filename):
    fo = open(filename)
    try:
        yield fo
    finally:
        fo.close()


# custom_open 函数一直运行到 yield 语句，然后将控制权交给 with，然后在 as f 部分将 yield 的 fo 赋值给 f
with custom_open("file.txt") as f:
    print(f.read())

```

应该遵循 Python 之禅 [The Zen of Python](https://peps.python.org/pep-0020/) 来决定何时使用哪种。 如果封装的逻辑量很大，则类的方法可能会更好。 而对于处理简单操作的情况，函数方法可能会更好。

###### yield

先学习斐波那契数列。

0、1、1、2、3、5、8、13、21、34、…

定义：*F*(0) = 0，*F*(1) = 1，*F*(n) = *F*(n - 1) + *F*(n - 2)（*n* ≥ 2，*n* ∈ N*）

**常规递归方式**

```python
def fab(n):
    if n <= 1:
        return n
    return fab(n - 1) + fab(n - 2)


print(fab(9))  # 34

```

```python
def fab(n):
    if n <= 1:
        return n
    return fab(n - 1) + fab(n - 2)


for n in range(10):
    print(fab(n), end=' ')  # 0 1 1 2 3 5 8 13 21 34 

```

**优化1**

```python
def fab(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


print(fab(9))  # 34

```

**优化2：逐步引出 yield 概念**

```python
def fab(max_n):
    n, a, b = 0, 0, 1
    while n < max_n:
        print(b, end=' ')
        a, b = b, a + b
        n += 1


fab(9)  # 1 1 2 3 5 8 13 21 34 

```

有经验的开发者会指出，直接在 fab 函数中用 print 打印数字会导致该函数可复用性较差，因为 fab 函数返回 None，其他函数无法获得该函数生成的数列。

要提高 fab 函数的可复用性，最好不要直接打印出数列，而是返回一个 List（为什么不用 return 返回每一步的值？因为 return 后的语句不会再执行）。

```python
def fab(max_n):
    n, a, b = 0, 0, 1
    L = []
    while n < max_n:
        L.append(b)
        a, b = b, a + b
        n += 1
    return L


print(fab(9))  # [1, 1, 2, 3, 5, 8, 13, 21, 34]

```

改写后的 fab 函数通过返回 List 能满足复用性的要求，但是 **更** 有经验的开发者会指出，该函数在运行中占用的内存会随着参数 max 的增大而增大，如果要控制内存占用，最好不要用 List 来保存中间结果，而是通过 iterable 对象来迭代（本质就是不把所有的值都追加到 List 中之后再 return 再遍历，而是每一步都 return 值，但是又必须得保证程序能够在 return 之后进入到下一步，即 next）。利用 iterable 可以把 fab 函数改写为一个支持 iterable 的 class。

```python
class Fab:
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n += 1
            return r
        raise StopIteration()  # 如果没有下一个元素，抛出 StopIteration 异常


for n in Fab(9):
    print(n, end=' ')  # 1 1 2 3 5 8 13 21 34 

```

Fab 类通过 \_\_next\_\_() 不断返回数列的下一个数，内存占用始终为常数。然而，使用 class 改写的这个版本，代码远远没有 fab 函数版本来得简洁。最终选择使用 `yield` 既能保持 fab 函数的简洁性，同时又可以获得 iterable 的效果。

```python
def fab(max_n):
    n, a, b = 0, 0, 1
    while n < max_n:
        yield b
        a, b = b, a + b
        n = n + 1


for f_n in fab(9):
    print(f_n, end=' ')  # 1 1 2 3 5 8 13 21 34 

```

简单地讲，yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，调用 fab(9) 不会执行 fab 函数，而是返回一个 iterable 对象。

在 for 循环执行时，每次循环都会执行 fab 函数内部的代码，执行到 yield b 时，fab 函数就 return 一个迭代值，然后中断执行，下次迭代时，代码从 yield b 的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，直到再次遇到 yield。

也可以手动调用 fab(9)，然后使用 Python 内建函数 next() 来获取迭代器的下一个元素，这样就可以更清楚地看到 fab 的执行流程。

```python
def fab(max_n):
    n, a, b = 0, 0, 1
    while n < max_n:
        yield b
        a, b = b, a + b
        n = n + 1


f_n = fab(9)
# 可以看出 fab(9) 是一个 generator 对象
# 要注意区分 fab 和 fab(9)，fab 是一个 generator function，而 fab(9) 是调用 fab 返回的一个 generator，好比类的定义和类的实例的区别
print(f_n)  # <generator object fab at 0x000001668A73D380>

print(next(f_n))  # 1
print(next(f_n))  # 1
print(next(f_n))  # 2
print(next(f_n))  # 3
print(next(f_n))  # 5
print(next(f_n))  # 8
print(next(f_n))  # 13
print(next(f_n))  # 21
print(next(f_n))  # 34

print(next(f_n))  # StopIteration
# 当函数执行结束时，generator 自动抛出 StopIteration 异常，表示迭代完成。在 for 循环里，无需处理 StopIteration 异常，循环会正常结束。

```

**总结**

一个带有 yield 的函数就是一个 generator，它和普通函数不同，生成一个 generator 看起来像函数调用，但不会执行任何函数代码，直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，并返回一个迭代值，下次执行时从 yield 的下一个语句继续执行。看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，每次中断都会通过 yield 返回当前的迭代值。

yield 的好处是显而易见的，把一个函数改写为一个 generator 就获得了迭代能力，比起用类的实例保存状态来计算下一个 next() 的值，不仅代码简洁，而且执行流程异常清晰。

简单来看。

```python
def show_many_words():
    yield 'hello'
    yield 'python'
    yield 'world'


# show_many_words 是一个生成器函数，它使用 yield 关键字返回了三个值
# 当 show_many_words 函数被调用时，它不会立即执行，而是返回一个生成器对象。
# 每次调用生成器对象的 __next__() 方法时，函数会从上一次中断的位置继续执行，直到遇到下一个 yield 关键字。

# 可以使用 for 循环来迭代生成器对象，从而逐个获取生成器函数返回的值
for word in show_many_words():
    print(word)

```

### Dynamic typing

Python 是动态类型语言，变量并不是计算机内存中被写入的某个值（给变量赋的那个值才是），它们只是指向内存的标签或名称。因此可能存在这样的情况，变量 `a` 先代表值1，然后变成字符串 `a string`, 然后又变为指向一个函数。

因此，需要避免对不同类型的对象使用同一个变量名。

```python
# bad

a = 1
a = 'a string'


def a():
    pass


# good
count = 1
msg = 'a string'


def func():
    pass  # 实现代码

```

即使是相关的不同类型的对象，也建议使用不同命名。

```python
# bad
items = 'a b c d a b c d'
items = items.split(' ')  # ...变为列表
items = set(items)  # ...再变为集合

```

避免给同一个变量命名重复赋值是个好的做法。

### Mutable and immutable types

典型的动态类型包括列表与字典，不可变类型没有修改自身内容的方法。

比如，赋值为整数6的变量 x 并没有自增方法，如果需要计算 x + 1，必须创建另一个整数变量并给其命名。

```python
x = 6
x = x + 1  # x 变量是一个新的变量
```

元组是不可修改的。

字符串是不可变类型。这意味着当组合一个字符串时，需要将每一部分放到一个可变列表里，使用字符串时再 join 的做法更高效。

创建将0到19连接起来的字符串（例`012..1819`）。

```python
# bad
s1 = ''
for i in range(20):
    s1 += str(i)
print(s1)

# good
s2 = []
for i in range(20):
    s2.append(str(i))

print("".join(s2))

# better 1
s3 = [str(i) for i in range(20)]  # 使用列表推导的构造方式比在循环中调用 append() 来构造列表更好也更快
print("".join(s3))

# better 2
# map(function, iterable) 根据提供的函数对指定序列做映射，并返回一个列表
s4 = map(str, range(20))
print("".join(s4))

```

关于字符串的说明的一点是，使用 join() 并不总是最好的选择。比如当用预先确定数量的字符串创建一个新的字符串时，使用加法操作符确实更快，但在上文提到的情况下或添加到已存在字符串的情况下，使用 join() 是更好的选择。

```python
foo = 'foo'
bar = 'bar'

# good
foobar = foo + bar

# bad
# foo += 'ooo'

# good
foo = ''.join([foo, 'ooo'])

```

除了 `str.join()` 和 `+`，也可以使用 % 格式运算符来连接确定数量的字符串，但 [PEP 3101](https://peps.python.org/pep-3101/) 建议使用 `str.format()` 替代 % 操作符。

```python
foo = 'foo'
bar = 'bar'

foobar_1 = '%s%s' % (foo, bar)  # OK
foobar_2 = '{0}{1}'.format(foo, bar)  # BETTER
foobar_3 = '{foo}{bar}'.format(foo=foo, bar=bar)  # BEST

```

#### 字符串格式化

##### % 占位符

%s 匹配字符串，%d 匹配整数，%c 匹配字符，%f 匹配浮点数

```python
s1 = "hello %s" % 'world'
print(s1)

s2 = "hello %d" % 17
print(s2)

s3 = "hello %c" % 'X'
print(s3)

s4 = "hello %f" % 3.14
print(s4)

```

##### str.format()

使用 `{}` 做占位符。

```python
# 默认映射
s1 = "{} {}".format('hello', 'world')
print(s1)  # 'hello world'

# 位置映射（注意索引不能超出范围）
# 字符串的占位符与 format 参数不要求前后位置一一对应，只要索引位置对应即可
s2 = "{1} {0}".format('hello', 'world')
print(s2)  # 'world hello'

# 参数映射
s3 = "{p0} {p1}".format(p0='hello', p1='world')
print(s3)  # 'hello world'

```

## Code Style

### Explicit code

Python 提倡最明确和直接的编码方式。

```python
# bad
def make_complex_bad(*args):
    x, y = args
    return dict(**locals())


# good
def make_complex_good(x, y):
    return {'x': x, 'y': y}

```

#### locals()

以字典类型返回当前位置的全部局部变量。

```python
def test_locals(*args):
    x, y = args
    return locals()


print(test_locals(1, 2))

```

### One statement per line

在同一行代码中写两条独立的语句是糟糕的。

```python
# bad
if <complex-comparison> and <other-complex-comparison>:
    # do something
    
# good
cond1 = <complex-comparison>
cond2 = <other-complex-comparison>
if cond1 and cond2:
    # do something
```

### Function arguments

#### Positional arguments

例如，有两个函数 `send(message, recipient)` 或 `point(x, y)`，在调用的时候可以使用参数名称，也可以改变参数的顺序，如 `send(recipient='World', message='Hello')` 和 `point(y=2, x=1)`，但和 `send( 'Hello', 'World')` 和 `point(1, 2)` 比起来，这降低了可读性，而且带来了不必要的冗长，因此不推荐。

#### Keyword arguments

比如，一个更完整的 `send` 函数可以被定义为 `send(message, to, cc=None, bcc=None)`。这里的 `cc` 和 `bcc` 是可选的， 当没有传递给它们其他值的时候，它们的值就是None。可以按定义中的参数顺序而无需明确的命名参数来调用函数，就像 `send('Hello', 'World', 'Cthulhu', 'God')`。也可以使用命名参数而无需遵循参数顺序来调用函数，就像 `send('Hello again', 'World', bcc='God', cc='Cthulhu')` 。如果没有任何强有力的理由不去遵循最接近函数定义的语法：`send('Hello', 'World', cc='Cthulhu', bcc='God')` 那么这两种方式都应该是要极力避免的。

#### Arbitrary argument list

如果函数的目的是能够通过带有可扩展数目的位置参数的签名得到更好的表达，该函数可以被定义成 `*args` 的结构。在这个函数体中，`args` 是一个元组，它包含所有剩余的位置参数。举个例子，可以用任何容器作为参数去调用 `send(message, *args)`，比如 `send('Hello', 'God', 'Mom', 'Cthulhu')`。 在此函数体中，`args` 相当于 `('God','Mom', 'Cthulhu')`。

尽管如此，这种结构有一些缺点，使用时应该予以注意。如果一个函数接受的参数列表具有相同的性质，通常把它定义成一个参数，这个参数是一个列表或者其他任何序列会更清晰。在这里，如果 `send` 参数有多个容器（recipients），将之定义成 `send(message, recipients)` 会更明确，调用它时就使用 `send('Hello', ['God', 'Mom', 'Cthulhu'])`。这样的话，函数的使用者可以事先将容器列表维护成列表（list）形式，这为传递各种不能被解包成其他序列的序列（包括迭代器）带来了可能。

#### Arbitrary keyword argument dictionary

如果函数要求一系列待定的命名参数，可以使用 `**kwargs` 的结构。在函数体中 `kwargs` 是一个字典，它包含所有传递给函数但没有被其他关键字参数捕捉的命名参数。

和 arbitrary argument list 中所需注意的一样，相似的原因是：这些强大的技术是用在被证明确实需要用到它们的时候，它们不应该被用在能用更简单和更明确的结构，来足够表达函数意图的情况中。如对于函数 `send(message, **kwargs)` 使用 `send("hello", name="world", age=18, sex="male")` 完全可以使用 `send("hello", {"name": "world", "age": 18, "sex": "male"})` 形式。

### Public、Protected and Private

任何不开放给客户端代码使用的方法或属性，应该有一个下划线前缀。

```python
# 一个包含 protected 和 private 的类
class Foo:
    def __init__(self):
        # 一个下划线表示一个 protected 成员
        self._protected = 1
        # 两个下划线表示一个 private 成员
        self.__private = 2

    def _protected_method(self):
        return self._protected

    def __private_method(self):
        return self.__private

    def public_method(self):
        return self._protected_method(), self.__private_method()


foo = Foo()
print(foo.public_method())  # (1, 2)
print(foo._protected_method())  # 1
# print(foo.__private_method())  # AttributeError: 'Foo' object has no attribute '__private_method'. Did you mean: '_Foo__private_method'?

```

可以看出，受保护成员（protected）和公共成员（public）基本上没区别，在类的外部也可以通过实例对象调用，但会给出 `Access to a protected member _protected_method of a class` 的警告提示，私有成员（private）在类的外部被调用的时候，会给出 `Unresolved attribute reference '__private_method' for class 'Foo' ` 的警告提示，在代码运行过程中，会提示 `AttributeError: 'Foo' object has no attribute '__private_method'. Did you mean: '_Foo__private_method'?` 错误。

但 PyCharm 同样给出代码提示，表示 `__private_method` 是否使用 `_Foo__private_method` 代替，也就是说私有成员依旧可以通过 `object._className__memberName` 的方式被访问（属性）和调用（方法）。

```python
print(foo._Foo__private_method())  # 2

```

Python 没有内置的访问控制关键字，Python 社区更愿意依靠一组约定，来表明这些元素不应该被直接访问。Python 的 **显式优于隐晦** 原则在这里同样适用：如果需要访问一个以下划线开头的属性或方法，那么最好是在类的内部通过其他公有方法来实现。

### Returning values

当一个函数变得复杂，在函数体中使用多返回值的语句并不少见。然而，为了保持函数的明确意图以及一个可持续的可读水平，更建议在函数体中避免使用返回多个有意义的值。

在函数中返回结果主要有两种情况：函数正常运行并返回它的结果，以及错误的情况。如果在面对第二种情况时不想抛出异常，返回一个值（比如说 None 或 False）来表明函数无法正确运行，可能是需要的。在这种情况下，越早返回所发现的不正确上下文越好。 这将帮助扁平化函数的结构：在因为错误而返回的语句后的所有代码能够假定条件满足接下来的函数主要结果的运算。

```python
def process_data(data):
    if not data:
        return None  # 早期返回错误
    if not isinstance(data, list):
        return False  # 早期返回错误

    # 正常处理逻辑
    result = [x * 2 for x in data]
    return result
```

尽管如此，当一个函数在其正常过程中有多个主要出口点时，它会变得难以调试和返回其结果，所以保持单个出口点可能会更好。

```python
def process_data(data):
    if not data:
        return None  # 早期返回错误
    if not isinstance(data, list):
        return False  # 早期返回错误

    try:
        # 模拟计算，可能会发生异常
        result = [x * 2 for x in data]  # 如果成功了，也要抵制住返回 result 的诱惑
    except Exception as e:
        print(f"Error during calculation: {e}")
        return None

    # 如果 result 计算失败，尝试 Plan B
    if result is None:
        try:
            result = [x ** 2 for x in data]  # Plan B 计算
        except Exception as e:
            print(f"Error during Plan B calculation: {e}")
            return None

    # 返回最终结果 x
    return result

```

### Idiom

编程习语，说得简单些，就是写代码的方式。采用习语的 Python 代码通常被称为 Pythonic。

#### Unpacking

对列表或元组可以进行解包操作。

```python
# 常规解包
a, b = [1, 2]
print(a, b)  # 1 2

# 新方法
a, *b, c = [1, 2, 3, 4, 5]
print(a, b, c)  # 1 [2, 3, 4] 5

```

`enumerate()` 会对 List 或 Tuple 中的每个项提供包含两个元素的元组，一个是索引，一个是元素。

```python
list_of_numbers = [1, 2, 3, 4, 5]

for enum in enumerate(list_of_numbers):
    print(enum)
    
# 使用解包操作
for index, item in enumerate(list_of_numbers):
    print(index, item)

```

解包运算符 \* 和 \*\*，前者可以解包列表或元组成位置参数，后者可以解包字典成关键字参数。

```python
# *
def foo(*args):
    print(args)  # ('Zed', 'Shaw')
    arg1, arg2 = args
    print(f"arg1: {arg1}, arg2: {arg2}")


foo("Zed", "Shaw")  # arg1: Zed, arg2: Shaw


# **
def bar(**kwargs):
    print(kwargs)  # {'name': 'Zed', 'age': 37}
    for key, value in kwargs.items():
        print(f"{key}: {value}", end=", ")  # name: Zed, age: 37, 


bar(name="Zed", age=37)

```

#### Ignored variable

如果需要一个变量，但是不会用到这个变量，建议命名为 \_ 或 \_\_，这是不同的风格指南的不同建议。之所以出现这种不同建议，是因为 `_` 常用在作为 [`gettext()`](https://docs.python.org/zh-cn/3/library/gettext.html) 函数的别名，也被用在交互式命令行中记录最后一次操作的值。

```python
for __ in range(5):
    print('hello world')

```

### Searching for an item in a collection

如果需要在一个包含 **大量的项** 的数据集中查找一个项是否在其中，通常选择集合或字典而不是列表，列表中的查找是 O(n)，字典或集合中的查找是 O(1)，如果只有键而不是键/值对，可以选择一个集合（一种特殊类型的字典）。如果数据集真的很小（<1000个元素），列表的表现会相当不错。

### Zen of Python

[The Zen of Python](https://peps.python.org/pep-0020/)

例子：[幻灯片](https://github.com/hblanks/zen-of-python-by-example)

### Conventions

约定，其实就是 Python 语言规范。

#### Check IF statement

本着 `Expression can be simplified` 的原则，所以不需要在 `if` 语句中明确地比较一个变量是否为 True、False 还是 None（明确地比较，就是使用 `==` 的方式），直接写就可以。

```python
# bad
true_var = True

if true_var == True:
    print('hello True')

```

上述代码会给出 `Expression can be simplified` 的警告提示，并且给出 `Replace boolean expression with true_var` 的更正建议，PEP 8 则提示 `PEP 8: E712 comparison to True should be 'if cond is True:' or 'if cond:'`。

```python
# good
true_var = True

if true_var:
    print('hello True')

if not true_var:
    print('hello False')

```

首先，一个赋值为 `None` 的变量，转换成布尔类型的值为 `False`。

```python
none_var = None
print(bool(none_var))  # False

```

但是 `if` 语句中的 `None`，不能与 `False` 作判断。

```python
# bad
none_var = None

if none_var == False:
    print('hello None')

```

首先，上述代码无法输出预想的 `hello None`，PyCharm 给出建议 `Replace boolean expression with not true_var`，更正后可以正常输出。

```python
# Maybe better
none_var = None

if not none_var:
    print('hello None')  # hello None

```

但更好的做法是，使用 `is` 运算符，明确地比较 `None`。

```python
# good
none_var = None

if none_var is None:
    print('hello None')  # hello None

```

#### Access a Dictionary Element

不要直接 `dict['key']`，而应该做兼容性。

```python
# bad
d = {
    'hello': 'world'
}

# print(d['hi'])  # KeyError

# good
print(d.get('hi', 'default_value'))  # default_value

# Or
if 'hi' in d:
    print(d['hi'])

```

#### Short Ways to Manipulate Lists

**列表推导式** 提供了一种强大的方式来处理列表，**生成器表达式** 和列表推导式语法基本一致，但最终是返回一个生成器而不是一个列表。

生成器表达式可以创建一个可迭代的生成器对象，用于逐个生成结果，而不是一次性生成一个完整的列表。这表示生成器表达式具有惰性计算的特点，只有在需要的时候才会生成下一个元素，在处理大型数据集或无限序列时，可以节省内存。

而创建一个新的列表则需要做更多的工作，并且使用更多内存，如果只是遍历（loop）列表，优先考虑使用生成器。

如果真的需要创建第二个列表，例如需要很多次用到这个结果，再选择使用列表推导式。

```python
# 对比 List comprehensions 和 Generator expressions

items = [1, 2, 3, 4, 5]

# 推导式会创建一个新的列表对象
new_items_1 = [x for x in items if x % 2 == 0]
print(new_items_1)  # [2, 4]

# 生成器不会创建另一个列表，只是迭代原始列表
new_items_2 = (x for x in items if x % 2 == 0)
print(new_items_2)  # <generator object <genexpr> at 0x00000244936638B8>

```

通过上述代码可以看到，生成器表达式类似于列表推导式，但是使用圆括号 `()` 而不是方括号 `[]`，或者理解为实质上没有元组推导式，一直都是生成器。

如果是复杂的逻辑，使用 **生成器函数** 是个很好的选择。

```python
def make_batches(items, batch_size):
    current_batch = []
    for item in items:
        current_batch.append(item)
        if len(current_batch) == batch_size:
            yield current_batch
            current_batch = []
    yield current_batch


print(list(make_batches([1, 2, 3, 4, 5], batch_size=3)))  # [[1, 2, 3], [4, 5]]

```

##### Filtering a list

在迭代的过程中，永远不要从列表中移除元素。

```python
# bad
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 != 0:
        items.remove(item)

print(items)

# good
# 推导式或生成器

```

###### `filter()` 函数

语法：`filter(function, iterable)`，其中第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判断，然后返回 True 或 False，最后将返回 True 的元素放到生成器对象中。

```python
items = [1, 2, 3, 4, 5]

filtered_items = filter(lambda x: x % 2 == 0, items)
print(filtered_items)  # <filter object at 0x000001A54F1A66A0>
print(list(filtered_items))  # [2, 4]

```

##### Possible side effects of modifying the original list

如果有其他变量引用原始列表，则修改它可能会有风险。但如果真的想这样做，可以使用切片赋值（slice assignment）。

```python
items = [1, 2, 3, 4, 5]

items[:] = [x for x in items if x % 2 == 0]

# or
items[:] = (x for x in items if x % 2 == 0)

# or
items[:] = filter(lambda x: x % 2 == 0, items)

print(items)  # [2, 4]

```

##### Modifying the values in a list

赋值永远不会创建新对象。如果两个或多个变量引用相同的列表，则修改其中一个变量意味着将修改所有变量。

```python
# bad
items = [1, 2, 3, 4, 5]

items_copy = items  # 不会创建一个新的列表

for index in range(len(items)):
    items[index] += 3

print(items)  # [4, 5, 6, 7, 8]

print(items_copy)  # [4, 5, 6, 7, 8]

```

如果需要修改列表的值，创建一个新的列表对象并保留原始列表对象会更安全。

```python
# good
items = [1, 2, 3, 4, 5]

items_copy = items

items = [item + 3 for item in items]

print(items)  # [4, 5, 6, 7, 8]

print(items_copy)  # [1, 2, 3, 4, 5]

```

#### Line Continuations

当一个代码逻辑行的长度超过可接受的限度时，需要将之分为多个物理行。如果行的结尾是一个反斜杠，Python 解释器会把这些连续行拼接在一起。

```python
# bad
my_very_big_string = """For a long time I used to go to bed early. Sometimes, \
when I had put out my candle, my eyes would close so quickly \
that I had not even time to say “I’m going to sleep.”"""

print(my_very_big_string)

```

输出内容为：`For a long time I used to go to bed early. Sometimes, when I had put out my candle, my eyes would close so quickly that I had not even time to say “I’m going to sleep.”`。

如果不在行尾加反斜杠，就无法拼接成一个行，保持代码块中的样式。

```python
my_very_big_string = """For a long time I used to go to bed early. Sometimes, 
when I had put out my candle, my eyes would close so quickly 
that I had not even time to say “I’m going to sleep.”"""

print(my_very_big_string)

```

输出内容为：

```
For a long time I used to go to bed early. Sometimes, 
when I had put out my candle, my eyes would close so quickly 
that I had not even time to say “I’m going to sleep.”
```

但总是应该避免使用这种方式，因为它的脆弱性：如果在行的结尾，在反斜杠后加了空格，这会破坏代码。

```python
my_very_big_string = """For a long time I used to go to bed early. Sometimes, \ 
when I had put out my candle, my eyes would close so quickly \ 
that I had not even time to say “I’m going to sleep.”"""

print(my_very_big_string)

```

PyCharm 中会提示警告信息：`PEP 8: W605 invalid escape sequence '\ '`。

输出内容为：

```
For a long time I used to go to bed early. Sometimes, \ 
when I had put out my candle, my eyes would close so quickly \ 
that I had not even time to say “I’m going to sleep.”
```

可以看到反斜杠（`\`）没有起到它应有的作用，即拼接多个连续行。

一个更好的解决方案是在元素周围使用括号。左边以一个未闭合的括号开头，Python 解释器会把行的结尾和下一行连接起来直到遇到闭合的括号。同样的行为适用中括号和大括号。

```python
# good
my_very_big_string = (
    "For a long time I used to go to bed early. Sometimes, "
    "when I had put out my candle, my eyes would close so quickly "
    "that I had not even time to say “I’m going to sleep.”"
)

print(my_very_big_string)

```

这在从某个包中导入多个模块的时候很有用。

```python
# bad
from package1 import module1, module2, module3, \ 
    module4, module5, module6

```

如果反斜杠后多了一个空格，则提示警告信息：`Unused import statement 'from package1 import module1, module2, module3, \ module4, module5, module6' `，可以看到 IDE 识别成了 `\ module4`，这显然会破坏代码。

```python
# good
from package1 import (module1, module2, module3,
                      module4, module5, module6)

```

尽管如此，通常情况下，必须去分割一个长逻辑行意味着同时想做太多的事，这可能影响可读性。

## Common Gotchas

有一些陷阱。

### Mutable Default Arguments

先看一个，可变默认参数。

```python
def append_to(ele, to=[]):
    to.append(ele)
    return to


print(append_to(12))
print(append_to(14))

```

本意是接收一个元素和一个空列表，函数调用的时候将元素追加到列表中，常规理解是每次调用函数就会创建一个新的列表，所以期待的结果应该是：

```
[12]
[42]
```

但事实却是：

```
[12]
[12, 14]
```

原因是当函数被定义时，Python 的默认参数就被创建一次，而不是每次调用函数的时候创建。上述案例中，当函数被定义时，一个新的列表就被创建一次，而且同一个列表在每次成功的调用中都被使用。

其实上述案例中的代码在 PyCharm 中也有警告提示信息：`Default argument value is mutable`，同时如果按照给出的建议 `Replace mutable default argument` 进行更正，结果如下：

```python
def append_to(ele, to=None):
    if to is None:
        to = []
    to.append(ele)
    return to


print(append_to(12))
print(append_to(14))

```

### Late Binding Closures

再看一个，延迟绑定闭包。

```python
items = []

for i in range(5):
    def item(x):
        return i * x


    items.append(item)

for f in items:
    print(f(5))

```

预想当中，`items` 是一个包含五个函数的列表，其中每个函数有它们自己的封闭变量 `i` 乘以它们的参数，输出结果应该是：

```
0
5
10
15
20
```

但事实却是：

```
20
20
20
20
20
```

这种困惑往往发生在 Python 在闭包（或在周围全局作用域（surrounding global scope），本案例就是）中绑定变量的时候。

上述案例中，五个函数都被创建了，但全都是 `4` 乘以参数 `x`。

原因是 Python 的闭包是迟绑定。表示闭包中用到的变量的值，是在内部函数被调用时查询得到的。

在11行，函数被调用，此时 `i` 的值在周围作用域中查询到是循环完成之后的 `4`，所以此时的 `i` 始终都是 `4`。解决方案是可以创建一个立即绑定参数的闭包。

```python
items = []

for i in range(5):
    def item(x, idx=i):  # 立即绑定参数
        return idx * x


    items.append(item)

for f in items:
    print(f(5))

```

上述案例如果放在闭包里面，应该是这样的：

```python
def create_items():
    items = []

    for i in range(5):
        def item(x, idx=i):  # 立即绑定参数
            return idx * x

        items.append(item)

    return items


for f in create_items():
    print(f(5))

```

或函数内部写成一个 lambda 函数：

```python
def create_items():
    return [lambda x, idx=i: x * idx for i in range(5)]


for f in create_items():
    print(f(5))

```



#### Closures

一个简单的闭包案例。

```python
def outer_func(n):
    def inner_func(x):
        return n * x

    return inner_func


f1 = outer_func(10)
print(f1(3))
print(f1(5))

```

上述案例中，8行的代码，实质上等价于：

```python
def inner_func(x):
    return 10 * x  # 这个数据 `10` 已经附加到了代码上
```

如何理解闭包，简单来说，外层函数嵌套内层函数，内层函数使用外层函数的变量，外层函数返回内层函数。

有这么一个需求，要求记录学习时间，以分钟进行累加。

所以定义一个全局变量，定义一个函数，接收一个参数用于新增每次的学习时间。

```python
study_time = 0


def study(time):
    study_time += time
    return study_time


print(study(5))
print(study(15))

```

期待输出：

```
5
20
```

但事实是 Python 会报错：`UnboundLocalError: local variable 'study_time' referenced before assignment`，意思是局部变量 `study_time` 在赋值前被引用。

因此局部变量在函数内部应该先出现赋值操作，再进行引用。

```python
def study(time):
    study_time = 0  # 先赋值
    study_time += time  # 再引用（修改）
    return study_time


print(study(5))  # 5
print(study(15))  # 15

```

为什么全局变量 `study_time` 没有起到作用？

```python
study_time = 0


def study():
    return study_time


print(study())  # 0

```

上述案例代码不会报错，正常输出全局变量 `study_time` 的值为 `0`，表示全局变量 `study_time` 起到了作用，但在本案例当中为什么不可以？

原因是如果在函数内部出现了和全局变量同名的变量，并且对其在赋值之前进行了引用（修改），该变量就变成了局部变量。

如果确定要使用全局变量，应该使用 `global` 关键字。

```python
study_time = 0


def study(time):
    global study_time  # 表示是全局变量而不是局部变量
    study_time += time
    return study_time


print(study(5))  # 5
print(study(15))  # 20

```

但始终应该尽量避免使用全局变量，因为它的不可预知性。

恰恰，闭包可以避免使用全局值，并提供某种形式的数据隐藏。

```python
time = 0


def add_study_time(total_time):
    def study(study_time):
        nonlocal total_time  # `nonlocal` 关键字只能在嵌套函数中使用，而不能在全局作用域中使用。它用于解决内层函数无法直接访问外层函数的变量的问题。
        total_time += study_time
        return total_time

    return study


print(time)  # 0
f = add_study_time(time)
print(f(5))  # 5
print(time)  # 0
print(f(15))  # 20
print(time)  # 0

```

最直接的表现就是全局变量 `time` 至此至终都没有修改过。

当某个函数被当成对象返回时，夹带了外部变量，就形成了一个闭包。
