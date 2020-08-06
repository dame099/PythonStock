import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):    #MyWindow가 QMainWindow를 상속함
    def __init__(self):
        super().__init__()  #부모클래스(super)의 init을 호출, 부모클래스의 인스턴스 변수까지 상속받는다.
        self.setWindowTitle("PyStock")
        self.setGeometry(300,300,300,400)

        btn1 = QPushButton("Click me",self)
        btn1.move(20,20)
        btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        QMessageBox.about(self,"message","clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()