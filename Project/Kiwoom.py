import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as  pd
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2

#모의투자 계좌번호 8145067911

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
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

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

    #종목코드에 해당하는 종목명을 반환하는 함수
    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
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

        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)

        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)

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

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))


    #주식 주문을 보내는 함수    
    def send_order(self,rqname,screen_no,acc_no,order_type,code,quantity,price,hoga,order_no):
        print(code)
        self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",[rqname,screen_no,acc_no,order_type,code,quantity,price,hoga,order_no])    

    #체결 잔고를 받아오는 함수, OnReceiveChejan이벤트가 호출될 때 그 안에서 사용해야 한다. 
    def get_chejan_data(self,fid):
        ret = self.dynamicCall("GetChejanData(int),fid")
        return ret

    #OnReceiveChejan이벤트를 처리해주는 함수
    def _receive_chejan_data(self,gubun,itme_cnt,fid_list):
        print(gubun)    #체결구분 접수와 체결시 '0'값, 국내주식 잔고전달은 '1'값, 파생잔고 전달은 '4'
        #fid값을 통해 서로 다른 데이터를 얻을 수 있다.
        print(self.get_chejan_data(9023))   #fid=9023, 주문번호
        print(self.get_chejan_data(302))    #fid=302, 종목명
        print(self.get_chejan_data(900))    #fid=900, 주문수량
        print(self.get_chejan_data(901))    #fid=901, 주문가격

    #로그인 사용자 정보를 얻어오는 함수
    def get_login_info(self,tag):
        ret = self.dynamicCall("GetLoginInfo(QString)",tag)
        return ret

    #계좌의 예수금(d+2)정보를 얻어오는 함수
    def _opw00001(self, rqname, trcode):
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(d2_deposit)

    #계좌의 평가잔고 데이터 및 보유 종목별 데이터를 읽어오는 함수
    def _opw00018(self,rqname,trcode):
        #싱글데이터를 통해 계좌 잔고관련 정보를 얻어오는 부분
        total_purchase_price = self._comm_get_data(trcode,"",rqname,0,"총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        #모의투자인 경우에는 총수익률 / 100을 해주어야 한다.
        if not self.get_server_gubun():
            total_earning_rate = float(total_earning_rate) / 100
            total_earning_rate = str(total_earning_rate)

        self.opw00018_output['single'].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_profit_loss_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_earning_rate))
        self.opw00018_output['single'].append(Kiwoom.change_format(estimated_deposit))

        #멀티데이터를 통해 보유종목 관련 데이터를 얻어오는 부분
        rows = self._get_repeat_cnt(trcode,rqname)
        #한번에 20개 종목만 조회 가능하므로 반복문을 통해 구현
        for i in range(rows):   
            name = self._comm_get_data(trcode,"",rqname,i,"종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            print(name)
            quantity = Kiwoom.change_format(quantity)
            purchase_price = Kiwoom.change_format(purchase_price)
            current_price = Kiwoom.change_format(current_price)
            eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(earning_rate)  #수익률은 change_format2함수를 통해 포맷 변경해준다.

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price,eval_profit_loss_price, earning_rate])
    
    def reset_opw00018_output(self):
        self.opw00018_output = {'single':[], 'multi':[]}

    #실서버와 모의투자 서버를 구분해주는 함수
    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret

########################
    #정적메서드 구현
########################
    #큰 숫자가 들어왔을때 가독성을 위해 쉼표를 표시해주는 함수
    @staticmethod 
    def change_format(data):
        strip_data = data.lstrip('-0')  #문자열의 왼쪽에 존재하는 '-' 또는 '0'을 제거
        if strip_data =='':
            strip_data = '0'    #0이 입력으로 들어온 경우

        #천의 자리마다 콤마를 추가, 책에서 긁어온거라 잘 모름.
        try:
            format_data = format(int(strip_data), ',d')
        except:
            format_data = format(float(strip_data))

        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data   
    def change_format2(data):
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        if strip_data.startswith('.'):
            strip_data = '0' + strip_data

        if data.startswith('-'):
            strip_data = '-' + strip_data

        return strip_data




if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    accouns_num = int(kiwoom.get_login_info("ACCOUNT_CNT"))
    accounts = kiwoom.get_login_info("ACCNO")

    #얻어온 계좌를 출력
    accounts_list = accounts.split(';')[0:accouns_num]
    print(accounts_list)

    kiwoom.set_input_value("계좌번호",accounts_list[0])
    kiwoom.set_input_value("비밀번호","1152")
    kiwoom.comm_rq_data("opw00001_req","opw00001",0,"2000")
    print(kiwoom.d2_deposit)

    kiwoom.set_input_value("계좌번호",accounts_list[0])
    kiwoom.comm_rq_data("opw00018_req","opw00018",0,"2000")
