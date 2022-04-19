# 什么是第一类对象

# 	1. 可作为对象赋值到一个变量
# 	2. 可作为元素添加到集合对象
# 	3. 可作为参数传递给其他函数
# 	4. 可当做函数的返回值

# 对象通用属性

# 	1. ID
# 	2. 类型
# 	3. 值

def foo():
    return 1


print(id(foo))
print(type(foo))
print(foo)

# 举例函数赋值到变量

# 赋值给另一个变量时，函数并不会被调用，只是在函数对象上绑定一个新名字，引用计数加一

bar = foo
b = foo
print(bar is b)

# 类也可作为函数
# 自定义类实现了 __call__ 方法，则该类的实例化对象的行为就是函数，是可以被调用 callback 的对象


class Add:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return x + self.n
    
add = Add(1)
print(add(2))
