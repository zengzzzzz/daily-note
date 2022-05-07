# 测试deepcopy的效率及对deepcopy的效率提高

import copy
import time
import pickle


array = [1 for i in range(1000)]

# deepcopy
st1  = time.time()
new_array = copy.deepcopy(array)
print(f"deepcopy: {time.time() - st1:.10f}")

# 赋值
st2  = time.time()
new_array = array
print(f"new: {time.time() - st2:.10f}")

# copy
st3  = time.time()
new_array = array.copy()
print(f"array.copy: {time.time() - st3:.10f}")

# copy
st4 = time.time()
new_array = array[:]
print(f"array[:]: {time.time() - st4:.10f}")

# deepcopy with pickle
st5 = time.time()
new_array = pickle.loads(pickle.dumps(array))
print(f"pickle: {time.time() - st5:.10f}")

# def deepcopy
class A:
    def __init__(self, b= 9):
        self.array = [1 for i in range(100)]
        self.b = b
    def __deepcopy__(self, memo):
        info = A()
        info.b = self.b
        return info

a = A(7)
st6 = time.time()
newa = copy.deepcopy(a)
print(f"def deepcopy: {time.time() - st6:.10f}")