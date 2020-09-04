import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")    #dynamicCall로 API의 CommConnect호출(로그인 이벤트)
        
        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)  #OnEventConnect가 발생한 경우, 새로운 이벤트로 연결
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        

        # SetUp Widget
        self.setWindowTitle("PyStock")
        self.setGeometry(300,300,300,150)

        label = QLabel('종목코드',self) #텍스트 출력, 두번째 인자는 부모 위젯
        label.move(20,20)   #label은 self의 다른 요소에서 사용되지 않으므로 self.label로 선언하지 않아도 된다.

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80,20)
        self.code_edit.setText("039490")    #기본종목코드

        btn1 = QPushButton("조회",self)
        btn1.move(190,20)
        btn1.clicked.connect(self.btn1_cliked)

        self.text_edit = QTextEdit(self)    #QTextEdit으로 조회 결과 출력
        self.text_edit.setGeometry(10,60,280,80)    
        self.text_edit.setEnabled(False)    #읽기모드로만 사용하기 위해서 False로 설정


    #로그인 정보
    def event_connect(self,err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")


    #종목 조회 함수
    def btn1_cliked(self):
        code = self.code_edit.text()
        self.text_edit.append("종목코드: " + code)
        #SetInputValue : 입력데이터 설정
        self.kiwoom.dynamicCall("SetInputValue(QString,QString)","종목코드",code)
        #CommRqData : TR(TRasaction)을 서버로 전송
        self.kiwoom.dynamicCall("CommRqData(Qstring,QString,int,QString)","opt10001_req","opt10001",0,"0101")



    #데이터 받기 함수
    #OnRecieveTrData(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2)
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            #CommGetData : 서버로부터 수신받은 데이터 가져오기
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")

            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()