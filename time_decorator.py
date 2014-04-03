import time

def my_decorator_time(function_to_decorate):
    def wrapper(*args, **kwargs):
        t=time.clock()
        function_to_decorate(*args, **kwargs) 
        print(time.clock()-t) 
    return wrapper
 
@my_decorator_time
def f(a, b):
    print(a+b)
    return a+b

f(1,1)
