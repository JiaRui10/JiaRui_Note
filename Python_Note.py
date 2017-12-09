             # 让Python程序变成一个可执行脚本
#!/usr/bin/env python

            # 装饰器
# 作用：对一个函数、方法或者类进行加工。提高了程序的可重复利用性，并增加了程序的可读性。
# ----------------------------->
def decorator(F):
    def new_F(a, b):
        print('input', a, b) # 添加一个打印输入功能
        return F(a, b)
    return new_F

@decorator
def square_sum(a, b):
    return a**2 + b**2

@decorator
def square_diff(a, b):
    return a**2 - b**2

print(square_sum(3, 4))
print(square_diff(3, 4))
# <-----------------------------

# ----------------------------->
# 含参的装饰器
def pre_str(pre=''):
    def decorator(F):
        def new_F(a, b):
            print(pre + 'input', a, b)
            return F(a, b)
        return new_F
    return decorator

@pre_str('^_^')
def square_sum(a, b):
    return a**2 + b**2

@pre_str('T_T')
def square_diff(a, b):
    return a**2 - b**2

print(square_sum(3, 4))
print(square_diff(3, 4))
# <-----------------------------

# ----------------------------->
# 装饰类
def decorator(aClass):
    class newClass:
        def __init__(self, age):
            self.total_display = 0
            self.wrapped = aClass(age)
        def display(self):
            self.total_display += 1
            print('total display', self.total_display)
            self.wrapped.display()
    return newClass

@decorator
class Bird:
    def __init__(self, age):
        self.age = age
    def display(self):
        print('My age is', self.age)

eagleLord = Bird(5)
for i in range(3):
    eagleLord.display()
# <-----------------------------


            # 内存管理
# 【对象的内存使用】
# ----------------------------->
a = 1   # 对象与引用分离。引用a指向对象1
print(id(a))    # 该对象的内存地址
print(hex(id(a)))
# <-----------------------------

# ----------------------------->
# Python会缓存整数和短小的字符
a = 1
b = 1
print(id(a))
print(id(b))    # 两个对象指向同一个引用
# <-----------------------------

# ----------------------------->
# is用于判断两个引用所指的对象是否相同
a = 1
b = 1
print(a is b)

a = 'good'
b = 'good'
print( a is b)

a = 'very good morning'
b = 'very good morning'
print(a is b)

a = []
b = []
print(a is b)

# 即使是赋值语句，也只是创造了新的引用，而不是对象本身。
# <-----------------------------

# 在Python中，每个对象都存有指向该对象的引用总数，即【引用计数】。
# 使用sys包中的getrefcount()，来查看某个对象的引用计数。getrefcount()所得到的结果，会比期望的多1.
# ----------------------------->
from sys import getrefcount

a = [1, 2, 3]
print(getrefcount(a))

b = a
print(getrefcount(b))
# <-----------------------------


#【对象引用对象】
# 容器对象中包含的并不是元素对象本身，是指向各个元素对象的引用。
# 自定义一个对象，并引用其他对象
# ----------------------------->
class from_obj(object):
    def __init__(self, to_obj):
        self.to_obj = to_obj

b = [1, 2, 3]
a = from_obj(b)     # a引用的对象b
print(id(a.to_obj))
print(id(b))
#<-----------------------------

# ----------------------------->
# 当一个对象A被另一个对象B引用时，A的引用计数将增加1
from sys import getrefcount

a = [1, 2, 3]
print(getrefcount(a))

b = [a, a]
print(getrefcount(a))
#<-----------------------------

# ----------------------------->
# 两个对象可能相互引用，从而构成所谓的引用环
a = []
b = [a]
a.append(b)
# 即使是一个对象，只需要自己引用自己，也能构成引用环
a = []
a.append(a)
print(getrefcount(a))
# 引用环会给垃圾回收机制带来很大的麻烦
#<-----------------------------


#【引用减少】
# ----------------------------->
from sys import getrefcount

a = [1, 2, 3]
b = a
print(getrefcount(b))

del a
print(getrefcount(b))
#<-----------------------------

# ----------------------------->
a = [1, 2, 3]
del a[0]
print(a)
#<-----------------------------

# ----------------------------->
from sys import getrefcount

a = [1, 2, 3]
b = a
print(getrefcount(b))

a = 1
print(getrefcount(b))
#<-----------------------------

# 没看完....