import win32com.client

instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

instStockChart.SetInputValue(0, "A003540")
#날짜개수로 요청
instStockChart.SetInputValue(1, ord('2'))
instStockChart.SetInputValue(4, 60) #60일치 요청
#기간으로 요청
# instStockChart.SetInputValue(1,ord('1'))
# instStockChart.SetInputValue(2,20200729)
# instStockChart.SetInputValue(3,20200720)
#다음부분은 모두 동일
instStockChart.SetInputValue(5, (8)) #거래량 요청
instStockChart.SetInputValue(6, ord('D')) #차트구분
instStockChart.SetInputValue(9, ord('1')) #수정주가 여부

instStockChart.BlockRequest()

#volumes에 거래량 저장
volumes = []
numData = instStockChart.GetHeaderValue(3)  #3번옵션은 전달받은 개수
for i in range(numData):
    volumes.append(instStockChart.GetDataValue(0,i))    

avgVolumes = (sum(volumes)-volumes[0])/(len(volumes)-1) #평균거래량 = 오늘 거래량을 제외한 평균

if(volumes[0]>avgVolumes*10):
    print("great!!!")
else:
    print("Nah...",round(volumes[0]/avgVolumes,5))