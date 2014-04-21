import sys, threading, subprocess
from PySide import QtCore, QtGui

class Pinger(QtGui.QWidget):

	def __init__(self, parent=None):
		super(Pinger, self).__init__(parent)

		IPLabel = QtGui.QLabel("IP:")
		self.IPaddress_text = QtGui.QTextEdit()

		LogLabel = QtGui.QLabel("LOG:")
		self.Log_text = QtGui.QTextEdit()
		self.Log_text.setReadOnly(True)

		self.PingButton = QtGui.QPushButton("PING")
		self.PingButton.show()

		self.PingButton.clicked.connect(self.Ping)

		self.count_threadSpinBox = QtGui.QSpinBox()
		self.count_threadSpinBox.setRange(1, 99)
		self.count_threadSpinBox.setSingleStep(1)
		self.count_threadSpinBox.setValue(10)

		self.count_threadSpinBox.valueChanged[int].connect(self.changed)
		self.count_thread=10

		mainLayout = QtGui.QGridLayout()
		mainLayout.addWidget(IPLabel, 0, 0)
		mainLayout.addWidget(self.IPaddress_text, 0, 1)
		mainLayout.addWidget(LogLabel, 1, 0)
		mainLayout.addWidget(self.Log_text, 1, 1)
		mainLayout.addWidget(self.PingButton, 2, 1)
		mainLayout.addWidget(self.count_threadSpinBox, 2, 0)

		self.setLayout(mainLayout)
		self.setWindowTitle("Ping")

	def changed(self, value):
		self.count_thread=value

	def Ping(self):
		self.massip=list(self.IPaddress_text.toPlainText().splitlines())
		self.Log_text.setText(ThreadPing(self.massip, self.count_thread).run())

class ThreadPing():
	def __init__(self, ips, NumberThreads):
		import queue
		self.NUMBER_THREADS=NumberThreads
		self.ip=queue.Queue()

		for x in ips:
			self.ip.put(x)
        
		self.threads= []
	def run(self):
		global res
		res=[]
		for x in range(self.NUMBER_THREADS):
			res.append('')
			self.threads.append(MyPing(self.ip, x))
			self.threads[-1].start()
		for x in range(self.NUMBER_THREADS):
			self.ip.join()
		print (res)
		return (''.join(res))

class MyPing(threading.Thread):
	def __init__(self, ip, x):
		super(MyPing,self).__init__()
		self.ip=ip
		self.x=x
	def run (self):
		while not self.ip.empty():
			CurrentIp=self.ip.get()
			result = subprocess.call("ping -c 1 %s" % CurrentIp,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
			if result==0:
				res[self.x]+='''<font color="green">%s</font><br>''' %CurrentIp
			else:
				res[self.x]+='''<font color="red">%s</font><br>''' %CurrentIp
			self.ip.task_done()
            
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	pinger = Pinger()
	pinger.show()
	sys.exit(app.exec_())
