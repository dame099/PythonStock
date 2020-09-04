from pandas import Series, DataFrame

daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

daeshin_day = DataFrame(daeshin,index=['0901','0902','0903','0904','0905'])
print(daeshin_day['open'])
print(daeshin_day.loc['0904'])  #loc = index로 조회, location
print(daeshin_day.columns)
print(daeshin_day.index)