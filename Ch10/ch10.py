import win32com.client


instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(1)

kospi = {}
for i,code in enumerate(codeList):
    name = instCpCodeMgr.CodeToName(code)
    kospi[code] = name
    secondCode = instCpCodeMgr.GetStockSectionKind(code)
    print(i, code, kospi[code], secondCode)
    if(name=='NAVER'):
        break

f = open("./kospi.csv",'w')
for i in kospi:
    f.write("%s,%s\n" % (i,kospi[i]))
f.close()