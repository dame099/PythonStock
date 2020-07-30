import win32com.client
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")



instStockChart.SetInputValue(0, "A003540")
#개수로 요청
#instStockChart.SetInputValue(1, ord('2'))
#instStockChart.SetInputValue(4, 10)
#기간으로 요청
instStockChart.SetInputValue(1,ord('1'))
instStockChart.SetInputValue(2,20200729)
instStockChart.SetInputValue(3,20200720)
#다음부분은 모두 동일
instStockChart.SetInputValue(5, (0,2,3,4,5,8))
instStockChart.SetInputValue(6, ord('D'))
instStockChart.SetInputValue(9, ord('1'))


instStockChart.BlockRequest()

numData = instStockChart.GetHeaderValue(3)
numFiled = instStockChart.GetHeaderValue(1)

for i in range(numData):
    for j in range(numFiled):
        print(instStockChart.GetDataValue(j,i),end=" ")
    print("")