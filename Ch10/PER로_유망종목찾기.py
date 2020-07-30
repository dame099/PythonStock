import win32com.client


#업종별 코드 리스트 조회
def LookUp_IndustryCode(instCpCodeMgr):
    industryCodeList = instCpCodeMgr.GetIndustryList()
    for industryCode in industryCodeList:
        print(industryCode,instCpCodeMgr.GetIndustryName(industryCode))

#특정 업종에 해당하는 종목코드조회, code=조회하고 싶은 업종코드
def LookUp_Code_ByIndustry(instCpCodeMgr,code):
    tarketCodeList = instCpCodeMgr.GetGroupCodeList(code)
    CodeList = []
    for Tcode in tarketCodeList:
        CodeList.append(Tcode)
        print(Tcode, instCpCodeMgr.CodeToName(Tcode))
    return CodeList #종목코드를 반환

#특정 업종의 avgPER계산
def Get_avgPER_ByCode(instMarketEye,CodeList):
    instMarketEye.SetInputValue(0,67)
    instMarketEye.SetInputValue(1,CodeList)
    instMarketEye.BlockRequest()
    numStock = instMarketEye.GetHeaderValue(2) #반환 개수
    sumPER = 0
    for i in range(numStock):
        sumPER +=instMarketEye.GetDataValue(0,i)
    print("AVG PER is ",sumPER/numStock)

if __name__ == "__main__":
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
    LookUp_IndustryCode(instCpCodeMgr)
    CodeList = LookUp_Code_ByIndustry(instCpCodeMgr,9)  #CodeList = 특정 업종에 해당하는 모든 종목의 코드를 저장
    Get_avgPER_ByCode(instMarketEye,CodeList)

