import sys
from PyQt5.QtWidgets import *
import Kiwoom

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()  #로그인 함수 호출
        self.get_code_list()



    def run(self):
        print("running")
        print(self.kosdaq_list[0:4])
        print(self.kosdaq_list[0:4])

    #코스피 시장과 코스닥 시장의 모든 종목코드를 가져와서 저장하는 함수
    def get_code_list(self):
        self.kospi_list = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_list = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()