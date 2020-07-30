import win32com.client

#객체 생성
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

#0번 옵션 : 조회할 항목 ( ex) 4=현재가, 67=PER, 70=EPS, 111=최근분기년월데이터 )
instMarketEye.SetInputValue(0,(4,67,70,111))
#1번옵션 : 조회할 종목 코드
instMarketEye.SetInputValue(1,"A003540")

instMarketEye.BlockRequest()

#첫번째인자 : 요청항목에 대한 인덱스
#두번째인자 : 요청종목에 대한 인덱스, 현재는 하나만 요청했으므로 0번만 존재
print("현재가: ", instMarketEye.GetDataValue(0, 0))
print("PER: ", instMarketEye.GetDataValue(1, 0))
print("EPS: ", instMarketEye.GetDataValue(2, 0))
print("최근분기년월: ", instMarketEye.GetDataValue(3, 0))