import queue, threading, subprocess, sys, socket, argparse

class MyPing(threading.Thread):
    '''
    Класс который будет извлекать IP из очереди и проверять их
    '''
    def __init__(self, ip, output):
        #Инициализируем родителя
        super(MyPing,self).__init__()
        self.output=output
        self.ip=ip
    def run (self):
        '''
        проверка pinga
        '''
            
        while not self.ip.empty():
            CurrentIp=self.ip.get()
            result = subprocess.call("ping -s 1 %s" % CurrentIp, 
                                  shell=True, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT)
            if result==0:
                self.output.write(CurrentIp+'\n')
                
            self.ip.task_done()
            
class ThreadPing():
    '''
    Обработчик потоков
    '''
    def __init__(self, ips, output,  NumberThreads):
        self.NUMBER_THREADS=NumberThreads
        #Создаем очередь IP
        self.ip=queue.Queue()
        
        #Обрабатывам исключения с открытием файла
        try:
            self.output=open(output, 'w')
        except OSError:
            print("OSError")
            exit()
        
        #Заполняем очередь
        for x in ips:
            self.ip.put(x)
        
        self.threads= []
    def run(self):
        for x in range(self.NUMBER_THREADS):
            self.threads.append(MyPing(self.ip, self.output))
            self.threads[-1].start()
        #Ждем опустошения очереди
        self.ip.join()
        self.output.close()

#Парсинг
parser = argparse.ArgumentParser()
parser.add_argument('-n', action='store', type=int, dest='n', default=10, help='Count threads')
parser.add_argument('-o', action='store', dest='o', default='ping.log', help='Output file')
parser.add_argument('-ip', action='store', help='Mass of IPaddress', nargs='+')
args = parser.parse_args(sys.argv[1:-1])

#Проверка на непустоту
if args.ip is None:
    exit()
#Проверка на корректность IP
for x in args.ip:
    try:
        socket.inet_aton(x)
    except socket.error: 
        args.ip.remove(x)

ThreadPing(args.ip, args.o, args.n).run()
