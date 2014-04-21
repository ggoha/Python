from PySide import QtGui, QtCore
class ImageViewer(QtGui.QWidget):
	def __init__(self):
		super(ImageViewer, self).__init__()

		self.openButton = QtGui.QPushButton("Open")
		self.openButton.show()
		self.openButton.clicked.connect(self.open)		

		self.imageLabel = QtGui.QLabel()
		self.imageLabel.setScaledContents(True)

		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setWidget(self.imageLabel)

		self.slider = QtGui.QSlider(QtCore.Qt.Vertical)
		self.slider.setEnabled(False)
		self.slider.setRange(-100, 100)
		self.slider.setSingleStep(1)
		self.slider.setValue(0)
		self.slider.valueChanged[int].connect(self.changed)

		mainLayout = QtGui.QGridLayout()
		mainLayout.addWidget(self.openButton, 0, 0)
		mainLayout.addWidget(self.scrollArea, 0, 1)
		mainLayout.addWidget(self.slider, 0, 2)

		
		self.setLayout(mainLayout)
		self.setWindowTitle("Image Viewer")
		self.resize(500, 400)

	def open(self):
		fileName,other = QtGui.QFileDialog.getOpenFileName(self, "Open File")
		if fileName:
			image = QtGui.QImage(fileName)
			if image.isNull():
				QtGui.QMessageBox.information(self, "Image Viewer",
						"Cannot load %s." % fileName)
				return

			self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
			self.resizeImage(1)
			self.slider.setValue(0)
			self.slider.setEnabled(True)

	def resizeImage(self, zoom):
		self.imageLabel.resize(zoom * self.imageLabel.pixmap().size())

	def changed(self, value):
		import math
		self.resizeImage(math.exp(value/100*math.log(2)))
		
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	imageViewer = ImageViewer()
	imageViewer.show()
	sys.exit(app.exec_())
