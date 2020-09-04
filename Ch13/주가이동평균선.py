import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt #그래프 그려주는 모듈

gs = web.DataReader("078930.KS","yahoo","2014-01-01","2020-09-04")
print(gs.tail())

new_gs = gs[gs['Volume']!=0]    #공휴일의 경우에는 거래양(volume)이 0이므로 데이터에서 제외하고 새로운 new_gs를 생성해준다.


days = [5,20,60,120]
ma_days = {5:'MA5',20:"MA20",60:"MA60",120:"MA120"}


#이동평균계산 + DataFrame에 저장
for day in days:
    #수정종가의 이동평균선 계산
    ma_day = round(new_gs["Adj Close"].rolling(window=day).mean(),1)  
    #gs[Adj Close] : 수정종가 데이터가 담긴 pandas series
    #rolling : 앞으로부터 특정 데이터만큼만 잘라주는 역할, window=5이므로 5개 데이터에 대해서만 연산을 실행하도록 해준다. 
    #mean() : 평균 구하는 함수
    #round(n,k) : 실수 n을 소수점아래 k자리까지만 표현

    #print(ma5.tail())

    new_gs.insert(len(new_gs.columns), ma_days[day], ma_day)  #new_gs에 계산한 ma5를 컬럼으로 추가. parameter : 추가될위치(int), 컬럼이름, 컬럼데이터가 담긴 series
    print(new_gs.tail())


#DataFrame을 바탕으로 그래프 그리기
#그래프 선 그리기
for day in days:
    plt.plot(new_gs.index,new_gs[ma_days[day]])
plt.legend(loc='best')  #legend:범례표시, loc='best'로 인자를 전달하면 알아서 적당한 위치에 범례표시
plt.grid()  #격자표시

plt.show()

