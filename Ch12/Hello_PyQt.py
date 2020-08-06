import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
label = QPushButton("Hello PyQt")
label.show()
app.exec_()