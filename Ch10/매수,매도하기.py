import win32com.client

instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")

instCpTdUtil.TradeInit()
accountNumber = instCpTdUtil.AccountNumber[0]
instCpTd0311