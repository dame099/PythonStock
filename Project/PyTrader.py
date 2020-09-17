import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *

form_class = uic.loadUiType("pytrader.ui")[0]

class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom =Kiwoom()
        self.kiwoom.comm_connect()

        self.timer = QTimer(self)
        self.timer.start(1000)  #1초
        self.timer.timeout.connect(self.timeout)    #1초마다 이벤트 발생

        self.lineEdit.textChanged.connect(self.code_changed)    #lineEdit에 변화가 생기면 code_changed메서드로 연결
        #키움 모듈을 사용해서 계좌수와 계좌 번호를 받아옴.
        accouns_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")

        #얻어온 계좌를 QCombox에 출력
        accounts_list = accounts.split(';')[0:accouns_num]
        print(accounts_list)
        self.comboBox.addItems(accounts_list)   #combox에 읽어온 계좌 입력

        #장 시작시 자동 주문이 수행되는지 나타내주는 변수
        self.trade_stocks_done = False

        #종목코드가 입력되면 해당 종목명을 출력
        self.lineEdit.textChanged.connect(self.code_changed)

        #현금매수 버튼을 누루면 주문이 이뤄지도록 구현
        self.pushButton.clicked.connect(self.send_order)

        #조회버튼의 기능 구현
        self.pushButton_2.clicked.connect(self.check_balance)

        # Timer2, 10초마다 실시간 조회를 위한 타이머
        self.timer2 = QTimer(self)
        self.timer2.start(1000*10)
        self.timer2.timeout.connect(self.timeout2)

        #미리 저장되어있는 buy_list.txt와 sell_list.txt를 읽어오는 함수를 호출
        self.load_buy_sell_list()

    #각종 시간 관련 트리거 함수
    def timeout(self):
        market_start_time = QTime(9,0,0)
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결중"
        else:
            state_msg = "서버 미연결중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)

        #9시가 되면 자동으로 리스트에 있는 주문을 실행하도록 구현
        if current_time > market_start_time and self.trade_stocks_done is False:
            self.trade_stocks()
            self.trade_stocks_done = True


    #종목코드 입력칸(lineEdit)에 값이 입력되면, API를 이용해서 해당 종목명을 lindEdit_2에 출력해주는 기능
    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    #주문을 전달하는 함수
    def send_order(self):
        order_type_looup = {'신규매수' : 1, '신규매도' : 2, '매수취소' : 3, '매도취소' : 4}
        hoga_lookup = {'지정가' : '00', "시장가" : '03'}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.spinBox_2.value()

        self.kiwoom.send_order("send_order_req","0101",account,order_type_looup[order_type],code,num,price,hoga_lookup[hoga],"")

    def check_balance(self):
        self.kiwoom.reset_opw00018_output()
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(';')[0]

        #계좌의 평가잔고 및 보유종목을 조회하는 부분
        self.kiwoom.set_input_value("계좌번호",account_number)
        self.kiwoom.comm_rq_data("opw00018_req","opw00018",0,"2000")
        #최대 20개 종목만 조회 가능하므로 그 이상이면 루프를 돈다.
        while self.kiwoom.remained_data:
            time.sleep(0.2)
            self.kiwoom.set_input_value("계좌번호", account_number)
            self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 2, "2000")

        #계좌의 예수금을 조회하는 부분
        self.kiwoom.set_input_value("계좌번호",account_number)
        self.kiwoom.comm_rq_data("opw00001_req","opw00001",0,"2000")

        #조회한 예수금을 QTableWidget에 출력
        item = QTableWidgetItem(self.kiwoom.d2_deposit)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.tableWidget.setItem(0, 0, item)

        #조회한 계좌 데이터를 QTableWidget에 출력
        for i in range(1,6):
            item = QTableWidgetItem(self.kiwoom.opw00018_output['single'][i - 1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)
        #아이템의 크기에 맞춰 행의 높이를 조절
        self.tableWidget.resizeRowsToContents()

        #보유 종목별 데이터를 출력, 코드 통째로 긁어온거라 잘 모름, 수정XXXXX
        # Item list
        item_count = len(self.kiwoom.opw00018_output['multi'])
        print(self.kiwoom.opw00018_output['multi'])
        self.tableWidget_2.setRowCount(item_count)
        for j in range(item_count):
            row = self.kiwoom.opw00018_output['multi'][j]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_2.setItem(j, i, item)

        self.tableWidget_2.resizeRowsToContents()

    def timeout2(self):
        if self.checkBox.isChecked():
            self.check_balance()

    #미리 저장되어있는 buy_list.txt와 sell_list.txt를 읽어서 QTableWidget에 출력하는 함수
    def load_buy_sell_list(self):
        f = open("./buy_list.txt",'rt',encoding='UTF8')
        buy_list = f.readlines()
        f.close()

        f = open("./sell_list.txt",'rt',encoding='UTF8')
        sell_list = f.readlines()
        f.close()

        row_count = len(buy_list) + len(sell_list)  #출력할 row의 갯수
        self.tableWidget_3.setRowCount(row_count)

        #buy_list 출력, 긁어왔다.
        for row in range(len(buy_list)):
            row_data = buy_list[row]
            splited_row_data = row_data.split(';')
            splited_row_data[1] = self.kiwoom.get_master_code_name(splited_row_data[1].rsplit())
            for col in range(len(splited_row_data)):
                item = QTableWidgetItem(splited_row_data[col].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget_3.setItem(row, col, item)

        #sell_list 출력, 긁어왔다.
        for row in range(len(sell_list)):
            row_data = sell_list[row]
            splited_row_data = row_data.split(';')
            splited_row_data[1] = self.kiwoom.get_master_code_name(splited_row_data[1].rsplit())
            for col in range(len(splited_row_data)):
                item = QTableWidgetItem(splited_row_data[col].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget_3.setItem(len(buy_list) + row, col, item)

        #QTableWidget에서의 행 크기 조정
        self.tableWidget_3.resizeRowsToContents()

    #매일 장이 시작되는 시점에 선정된 종목에 대해 주문하는 함수
    def trade_stocks(self):
        hoga_lookup = {'지정가' : '00', '시장가' : '03'}
        
        f = open("buy_list.txt", 'rt',encoding='UTF-8')
        buy_list = f.readlines()
        f.close()
        f = open("sell_list.txt", 'rt',encoding='UTF-8')
        sell_list = f.readlines()
        f.close()

        account = self.comboBox.currentText()   #주문에 필요한 계좌정보를 combobox에서 얻어옴.

        #매수 실행
        for row_data in buy_list:
            splited_row_data = row_data.split(';')
            hoga = splited_row_data[2]
            code = splited_row_data[1]
            num = splited_row_data[3]
            price = splited_row_data[4]
            
            #상태정보가 매수전일때에만 send_oredr() 호출
            if splited_row_data[5].rstrip() == '매수전':
                self.kiwoom.send_order("send_order_req","0101",account,1,code,num,price,hoga_lookup[hoga],"")

        #매수 실행 후 buy_list update
        for i,row_data in enumerate(buy_list):
            buy_list[i] = buy_list[i].replace("매수전","주문완료")
        f = open("./buy_list.txt",'wt')
        for row_data in buy_list:
            f.write(row_data)
        f.close()

        #매도 실행
        for row_data in sell_list:
            splited_row_data = row_data.split(';')
            hoga = splited_row_data[2]
            code = splited_row_data[1]
            num = splited_row_data[3]
            price = splited_row_data[4]
            
            #상태정보가 매도전일때에만 send_oredr() 호출
            if splited_row_data[5].rstrip() == '매도전':
                self.kiwoom.send_order("send_order_req","0101",account,2,code,num,price,hoga_lookup[hoga],"")

        #매도 실행 후 sell_list update
        for i,row_data in enumerate(sell_list):
            sell_list[i] = sell_list[i].replace("매도전","주문완료")
        f = open("./sell_list.txt",'wt')
        for row_data in sell_list:
            f.write(row_data)
        f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()