import logging

def decorator_log(path):
    logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s в \'%(module)s %(message)s на %(lineno)d строке',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename=path) 
    def my_decorator(func): 
        def wrapped(*args, **kwargs) :
            logging.info('была запущена функция')
            return func(*args, **kwargs)
        return wrapped
    return my_decorator
 
@decorator_log(r'E:\eclipse\work\test\my_app.log')
def decorated_function():
    print ('Hello world')

@decorator_log(r'E:\eclipse\work\test\my_app.log')
def calc(string):
    print (eval(string))

decorated_function()
calc('2+2')
