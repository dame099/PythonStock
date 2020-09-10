import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

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
        self.onReceiveTrData.connect(self._receive_tr_data)

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

    def set_input_value(self,id,value):
        self.dynamicCall("SetInputValue(QString,QString)",id,value)

    def comm_rq_data(self,rqname,trcode,next,screen_no):
        self.dynamicCall("CommRqData(QString,QString,int,QString)",rqname,trcode,next,screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self,code,real_type,field_name,index,item_name):
        ret = self.dynamicCall("CommGetData(QString,QString,QString,int,QString)",code,real_type,field_name,index,item_name)
        return ret.strip()

    def _get_repeat_cnt(self,trcode,rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString,QString)",trcode,rqname)
        return ret

if __name__ == '__main__':
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    code_list = kiwoom.get_code_list_by_market('0')
    for code in code_list:
        print(code,end=" ")