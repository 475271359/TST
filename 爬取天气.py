"""
目标网站： 2345天气网站
总目标：爬取北方大区所有城市的历史天气。
阶段性目标：爬取山东济南过去一年的天气数据。
输入内容：
分析网站：
待爬取页面：http://tianqi.2345.com/wea_history/54511.htm
待爬取数据：数据在js里面，http://tianqi.2345.com/t/wea_history/js/202001/54511_202001.js
构建循环，用request库，批量下载。
处理内容： 不是标准的json，
实现返回的javascript解析，得到目标数据。
对于javascript的json如何解析？ 使用tqInfos = demjson.decode(data)["tqInfo"]进行解析。

输出内容：
保存为csv
http://tianqi.2345.com/t/wea_history/js/202001/54511_202001.js
"""

#构造2019年全年的月份列表
import requests as re
import demjson
import numpy as np
import pandas as pd
global city



#list = [54237, 54161, 54347, 54453, 54471, 54433, 54353, 54497, 53892, 54449, 53698, 54534, 54602, 53982, 60259,
#            53986,57091, 58005, 57195, 60255, 57186, 53978, 57073, 71361, 57051, 54857, 54765, 54843, 54830, 54915,
#           54827,58024,54945, 54938, 54828, 54823, 54714]
list = [54347,54161]

def getHTMLText(url):  # 定义了一个函数，用于获取html的文本。
    try:
        r = re.get(url, timeout=30)
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常。
        r.encoding = r.apparent_encoding  # 从内容中分析，修正代码的编码方式。
        return r.text
    except:
        return "产生异常"

for x in list:
    year = 2019
    ymd = []
    bWendu = []
    yWendu = []
    tianqi = []
    fengxiang = []
    fengli = []
    aqi = []
    aqiInfo = []
    aqiLevel = []
    city_list = []
    all_datas = []
    datas = []
    months = ["{:d}{:0>2d}".format(year, month + 1) for month in range(12)]  # 列表生成式
    urls = ["http://tianqi.2345.com/t/wea_history/js/{}/".format(month) +str(x)+"_{}.js".format(month) for month in months]  # 列表生成器
    for url in urls:
        data = getHTMLText(url).lstrip("var weather_str=").rsplit(";")
        datas.append(data[0])
    for data in datas:
        tqInfos = demjson.decode(data)["tqInfo"]
        city = demjson.decode(data)["city"]
        all_datas.extend(x for x in tqInfos  if len(x)>0)

    for y in range(len(all_datas)):
        ymd.append(all_datas[y].get('ymd'))
        bWendu.append(all_datas[y].get('bWendu'))
        yWendu.append(all_datas[y].get('yWendu'))
        tianqi.append(all_datas[y].get('tianqi'))
        fengxiang.append(all_datas[y].get('fengxiang'))
        fengli.append(all_datas[y].get('fengli'))
        aqi.append(all_datas[y].get('aqi'))
        aqiInfo.append(all_datas[y].get('aqiInfo'))
        aqiLevel.append(all_datas[y].get('aqiLevel'))
        city_list.append(city)
    Tianqi_np=np.array([ymd,bWendu,yWendu,tianqi,fengxiang,fengli,aqi,aqiInfo,aqiLevel,city_list])
    Tianqi_df = pd.DataFrame(Tianqi_np,index=["ymd","bWendu","yWendu","tianqi","fengxiang","fengli","aqi","aqiInfo","aqiLevel","city_list"])
    Tianqi_df=pd.DataFrame(Tianqi_df.values.T, index=Tianqi_df.columns, columns=Tianqi_df.index)
    Tianqi_df.to_excel("C:/Users/86132/Desktop/"+city+".xlsx")

