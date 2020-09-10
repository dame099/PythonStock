import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as  pd
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2

###################################################################
#Kiwoom 객체
#OpenAPI+와 통신을 쉽게 할 수 있도록 만드는 객체
###################################################################
class Kiwoom(QAxWidget):    #OpenAPI+의 메서드를 호출하기 위해서는 QAxWidget이 필요하므로 상속받는다.
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    #OpenAPI+에 대한 객체 생성 함수
    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")    #COM오브젝트 생성

    #서버로부터 발생한 이벤트(signal)와 이를 처리할 메서드(slot)를 연결해주는 함수
    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    #로그인을 위한 함수
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    #로그인 성공 여부 출력 함수
    def _event_connect(self,err_code):
        if err_code == 0:
            print("connected")

        else:
            print("disconnected")

        self.login_event_loop.exit()

    #API의 GetCodeListByMarket를 dynamicCall을 이용해서 호출해주는 함수
    def get_code_list_by_market(self,market):
        code_list = self.dynamicCall("GetCodeListByMarket(Qstring)",market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self,code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)",code)
        return code_name

    #연결상태를 확인해주는 함수
    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret
    #API의 SetInputValue를 호출하는 함수, tran입력값을 서버통신 전에 입력한다.
    def set_input_value(self,id,value):
        self.dynamicCall("SetInputValue(QString,QString)",id,value)

    #Tran을 서버로 송신하는 함수.
    def comm_rq_data(self,rqname,trcode,next,screen_no):
        self.dynamicCall("CommRqData(QString,QString,int,QString)",rqname,trcode,next,screen_no)
        #요청이후 이벤트 루프를 생성해서 응답이 올때까지 대기한다.
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    #서버에서 TR처리가 발생 후 실제로 데이터를 가져오는 함수
    def _comm_get_data(self,code,real_type,field_name,index,item_name):
        ret = self.dynamicCall("CommGetData(QString,QString,QString,int,QString)",code,real_type,field_name,index,item_name)
        return ret.strip()  #문자열 양쪽의 공백 제거

    #TR요청에 대해 반환값이 몇개인지 확인하는 함수
    def _get_repeat_cnt(self,trcode,rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString,QString)",trcode,rqname)
        return ret

    #TR 요청 결과로 OnReceiveTrData이벤트가 발생했을때 처리해주는 함수
    def _receive_tr_data(self,screen_no,rqname,trcode,record_name,next,unused1,unused2,unused3,unused4):
        #한번에 900개 이상의 데이터를 받아올 수 없으므로, API에서 남은 데이터가 있으면 next반환값으로 2를 리턴한다.
        #따라서 next=2이면 계속해서 작업을 수행하도록 구현한다.
        if next == '2': 
            self.remained_data = True
        else:
            self.remained_data = False

        #rqname에 따라 각각의 tr을 구분하고 적절한 반응을 하도록 구현해준다.  
        if rqname == 'opt10081_req':   #rqname이 opt10081_req이면 해당 메소드를 호출
            self._opt10081(rqname,trcode)

        try:
            self.tr_event_loop.exit()   #comm_rq_data에서 시작한 이벤트 루프 종료
        except AttributeError:
            pass

    #opt_10081, 일봉데이터 요청을 처리해주는 함수
    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname) #얻어올 데이터 개수를 미리 계산

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    # opt10081 TR 요청
    kiwoom.set_input_value("종목코드", "039490")
    kiwoom.set_input_value("기준일자", "20200910")
    kiwoom.set_input_value("수정주가구분", 1)
    kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

    while kiwoom.remained_data == True:
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", "039490")
        kiwoom.set_input_value("기준일자", "20170224")
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")