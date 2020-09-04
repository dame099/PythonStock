import pandas_datareader.data as web    #웹상의 데이터를 DataFrame객체로 반환
import datetime #날짜표현용
import matplotlib.pyplot as plt #그래프 그려주는 모듈


start_day = datetime.datetime(2016,2,14)
end_day = datetime.datetime(2016,3,1)

# gs = web.DataReader("078930.KS","yahoo",start_day,end_day)  #웹에서 데이이터를 얻어옴. parameter: 종목코드,출처,시작,종료
# print(gs)

gs_all = web.DataReader("078930.KS","yahoo")
print(gs_all.info())

plt.plot(gs_all.index,gs_all['Low'])    #그래프 출력, parametr : row_index,data_list
plt.show()