1. deepcopy

   ```python
   array = [1 for i in range(1000)]
   
   # deepcopy
   st1  = time.time()
   new_array = copy.deepcopy(array)
   print(f"deepcopy: {time.time() - st1:.10f}")
   
   # deepcopy: 0.0177206993
   ```

   deepcopy （python 3.8）方法解析：

   deepcopy 是用来进行深层复制的，其逻辑要根据对象的不同发生变化，例如float int等可直接拷贝，对复杂对象则需要将各个属性都进行复制。deepcopy需要解决问题一：可能存在的循环引用（树结构）问题二：如何构建新对象作为对象的复制

   ```python
   def deepcopy(x, memo=None, _nil=[]):
       """Deep copy operation on arbitrary Python objects.
   
       See the module's __doc__ string for more info.
       """
   
       if memo is None:  # memo 控制循环引用
           memo = {}   
   
       d = id(x)
       y = memo.get(d, _nil)
       if y is not _nil:
           return y
   
       cls = type(x)
   
       copier = _deepcopy_dispatch.get(cls)
       if copier is not None:
           y = copier(x, memo)
       else:
           if issubclass(cls, type):
               y = _deepcopy_atomic(x, memo)
           else:
               copier = getattr(x, "__deepcopy__", None) #可自定义 deepcopy 方法
               if copier is not None:
                   y = copier(memo)
               else:
                   reductor = dispatch_table.get(cls)
                   if reductor:
                       rv = reductor(x)
                   else:
                       reductor = getattr(x, "__reduce_ex__", None)
                       if reductor is not None:
                           rv = reductor(4)
                       else:
                           reductor = getattr(x, "__reduce__", None)
                           if reductor:
                               rv = reductor()
                           else:
                               raise Error(
                                   "un(deep)copyable object of type %s" % cls)
                   if isinstance(rv, str):
                       y = x
                   else:
                       y = _reconstruct(x, memo, *rv)  # 构建新的对象
   
       # If is its own copy, don't memoize.
       if y is not x:
           memo[d] = y
           _keep_alive(x, memo) # Make sure x lives at least as long as d
       return y
   ```

   解决一：  通过 memo 解决循环引用问题，带来性能损耗

   ```python
   # 构建新的对象，deepcopy 情况下是复制对象序列化的表示,再根据这个表示构建对象的复制
   def _reconstruct(x, memo, func, args,  
                    state=None, listiter=None, dictiter=None,
                    deepcopy=deepcopy):
       deep = memo is not None
       if deep and args:
           args = (deepcopy(arg, memo) for arg in args)
       y = func(*args)
       if deep:
           memo[id(x)] = y
   
       if state is not None:
           if deep:
               state = deepcopy(state, memo)
           if hasattr(y, '__setstate__'):
               y.__setstate__(state)
           else:
               if isinstance(state, tuple) and len(state) == 2:
                   state, slotstate = state
               else:
                   slotstate = None
               if state is not None:
                   y.__dict__.update(state)
               if slotstate is not None:
                   for key, value in slotstate.items():
                       setattr(y, key, value)
   
       if listiter is not None:
           if deep:
               for item in listiter:
                   item = deepcopy(item, memo)
                   y.append(item)
           else:
               for item in listiter:
                   y.append(item)
       if dictiter is not None:
           if deep:
               for key, value in dictiter:
                   key = deepcopy(key, memo)
                   value = deepcopy(value, memo)
                   y[key] = value
           else:
               for key, value in dictiter:
                   y[key] = value
       return y
   ```

   解决二：可自定义 __deepcopy 实现； 可通过 对象的reduce 或者 reduce_ex 获取对象的序列化表示，再进行复制，构建新的对象

   总结： deepcopy 简单粗暴，但其性能由于memo的原因较差。

2. 重写deepcopy

   根据deepcopy 中的建议，可自定义实现 deepcopy方法 ，仅复制所需要的值。

   ```python
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
   
   # def deepcopy: 0.0000321865
   ```

   总结：因仅复制所需要的值，则其性能是好于原生deepcopy的 ，但根据deepcopy源码解读，仍存在memo的问题。

3. pickle 序列化实现深拷贝

   根据python官方文档在copy模块中的注释，可使用pickle模块来序列化与反序列化来进行复制操作的。

   ```python
   array = [1 for i in range(1000)]
   
   # deepcopy with pickle
   st5 = time.time()
   new_array = pickle.loads(pickle.dumps(array))
   print(f"pickle: {time.time() - st5:.10f}")
   
   # pickle: 0.0009601116
   ```

   总结： 可实现，其性能是优于deepcopy的，但由于序列化的存在，性能并不是很理想

4. copy

   在该处并未涉及到对深层对象的修改，仅存在对第一层对象的修改，则使用copy也可实现基本使用。

   ```python
   array = [1 for i in range(1000)]
   
   # copy
   st3  = time.time()
   new_array = copy.copy(array)
   print(f"array.copy: {time.time() - st3:.10f}")
   
   # copy
   st4 = time.time()
   new_array = array[:]
   print(f"array[:]: {time.time() - st4:.10f}")
   
   
   #array.copy: 0.0000157356
   #array[:]: 0.0000178814
   ```

   总结： 以上俩种方式都为浅拷贝，可满足我们的需求。

上述方法所耗用时间（仅自测）deepcopy > pickle > 自定义 deepcopy > copy ，则在该处我们选择copy做浅拷贝即可。由此引起的思考，在该处我们可使用copy做浅拷贝使用，若是存在需要深层修改的部分，则应该考虑俩个方向的优化：一是自定义deepcopy方法，仅copy我们所需要的部分；二是在自定义deepcopy的基础上进行优化，无特殊循环引用的情况下可去掉memo这部分，提高性能。
在我们的实际使用中，应该关注传值或传引用的问题，避免在传引用的情况下仍然对对象进行修改，导致属性被覆盖的情况。对程序、对编码始终怀有敬畏之心。
