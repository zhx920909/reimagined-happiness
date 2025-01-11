# The Zen（禅） of Python

# Beautiful is better than ugly.

"""
Give me a function that takes a list of numbers and returns only the
even ones, divided by two.
"""


# 1. 使用列表管理返回值，缺点是列表的长度会增加，从而占用更多的内存。
# def halve_evens_only(nums):
#     result = []
#     for num in nums:
#         if num % 2 == 0:
#             # yield num / 2
#             result.append(num / 2)
#     return result

# 2. 使用生成器管理返回值，优点是惰性加载。
# def halve_evens_only(nums):
#     for num in nums:
#         if num % 2 == 0:
#             yield num / 2


# 上述两个案例主要是说明返回值使用列表和生成器的区别。

# 1.2 对 1 进行美化
# def halve_evens_only(nums):
#     return [num / 2 for num in nums if num % 2 == 0]

# 1.3 对 1.2 进行美化
# num 为偶数的时候，num % 2 == 0
# 0 转换为 bool 类型为 False
# not num % 2 为 True
# def halve_evens_only(nums):
#     return [num / 2 for num in nums if not num % 2]

# 以上是 Beautiful
# 下面介绍 Ugly

# 3. 使用 lambda 函数
# halve_evens_only = lambda nums: [num / 2 for num in nums if not num % 2]

# 3.1 再加上 map 函数
# halve_evens_only = lambda nums: map(lambda num: num / 2, [num for num in nums if not num % 2])

# 3.2 使用迭代器，要注意和生成器的区别
# halve_evens_only = lambda nums: map(lambda num: num / 2, filter(lambda num: not num % 2, nums))

# ls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# for res in halve_evens_only(ls):
#     print(res)

# Extend

# 1. map 函数，根据提供的函数对指定序列做映射，第一个参数 function 以第二个参数 iterable 中的每一个元素进行调用，返回包含每次调用后返回值的迭代器
# def square(x):
#     return x * x
#
#
# print(map(square, [1, 3, 5, 7, 9]))  # map object
# print(list(map(square, [1, 3, 5, 7, 9])))
#
# for i in map(square, [1, 3, 5, 7, 9]):
#     print(i)
#
# for i in map(lambda x: x ** 2, [1, 3, 5, 7, 9]):
#     print(i)

# 2. filter 函数，根据提供的函数对指定序列做过滤，第一个参数 function 以第二个参数 iterable 中的每一个元素进行调用，返回包含每次调用后返回值为 True 的迭代器
def is_even(num):
    return num % 2


for i in filter(is_even, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    print(i)

for i in filter(lambda num: num % 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    print(i)
