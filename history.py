# -*- coding: utf-8 -*-

"""
数据来源为丁香园疫情实时动态
https://ncov.dxy.cn/ncovh5/view/pneumonia
"""

import requests  # 发送请求
import re  # 正则表达式
import json
from datetime import datetime
import pandas as pd
import os

# 获取网页源代码
url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
page = requests.get(url, headers=headers).content.decode("utf-8")
UpdateTime = str(datetime.now()).split(' ')[0]

# 先保存json文件，以备不时之需
directory = "C:/Users/hasee/Desktop/pa/"  # 定义数据保存路径
filename = directory + UpdateTime + "_DXY.json"
with open(filename, "w", encoding="utf-8") as f:
    f.write(page)
    f.close()
# 以下代码用于打开json文件
# d = open(filename, "r", encoding="utf-8")
# content = d.read()
# d.close()

# 正则表达式提取信息
reg = '<script id="getListByCountryTypeService2true">([^<]+)'
data1 = re.findall(reg, page)[0][48:-11]
reg = '<script id="getTimelineService2">([^<]+)'
data2 = re.findall(reg, page)[0][35:-11]
reg = '<script id="getAreaStat">([^<]+)'
data3 = re.findall(reg, page)[0][27:-11]
reg = '<script id="fetchWHOArticle">([^<]+)'
data4 = re.findall(reg, page)[0][31:-11]
reg = '<script id="fetchGoodsGuide">([^<]+)'
data5 = re.findall(reg, page)[0][31:-11]
reg = '<script id="getIndexRecommendListundefined">([^<]+)'
data6 = re.findall(reg, page)[0][46:-11]
reg = '<script id="getIndexRumorList">([^<]+)'
data7 = re.findall(reg, page)[0][33:-11]
reg = '<script id="getStatisticsService">([^<]+)'
data8 = re.findall(reg, page)[0][36:-11]
reg = '<script id="getTimelineService1">([^<]+)'
data9 = re.findall(reg, page)[0][35:-11]
reg = '<script id="getWikiList">([^<]+)'
data10 = re.findall(reg, page)[0][27:-11]

# json格式转换为python格式数据
for i in range(1, 11):
    j = 'data' + str(i)
    exec(j + ' = json.loads(eval(j))')
    # globals()[j] = json.loads(eval(j))  # 与上一行代码效果相同，字符串转换为变量名，动态赋值

base_dir = directory + 'countryHistory/'
if not os.path.exists(base_dir):
    os.mkdir(base_dir)
# 解析数据
for item in data1:
    # 13位时间戳转换为字符串日期
    for key in item.keys():
        if key in ['createTime', 'modifyTime']:
            item[key] = datetime.fromtimestamp(item[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
    # 保存每个国家的历史数据
    if 'statisticsData' in item.keys():
        url = item['statisticsData']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        dailydata = requests.get(url=url, headers=headers).json()['data']
        df = pd.DataFrame(dailydata)
        df['countryFullName'] = item['countryFullName']
        df['countryName'] = item['provinceName']
        filename = base_dir + item['countryFullName'] + UpdateTime + '_history.csv'
        df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# 保存全球各国数据
for row in data1:
    if 'incrVo' in row.keys():
        # row['currentConfirmedIncr'] = row['incrVo']['currentConfirmedIncr']  # 现存确诊新增
        # row['confirmedIncr'] = row['incrVo']['confirmedIncr']   # 确诊新增
        # row['curedIncr'] = row['incrVo']['curedIncr']  # 治愈新增
        # row['deadIncr'] = row['incrVo']['deadIncr']  # 死亡新增
        # 效果相同的代码：
        for i in ['currentConfirmedIncr', 'confirmedIncr', 'curedIncr', 'deadIncr']:
            row[i] = row['incrVo'][i]
    # row.pop('incrVo')  可选择删除无用的数据
df = pd.DataFrame(data1)
filename = directory + UpdateTime + '_globalRealtime.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# 中国各城市实时数据
CityData = pd.DataFrame()  # 新建空dataframe
for row in data3:
    Citydf = pd.DataFrame(row['cities'])
    Citydf['provinceName'] = row['provinceName']
    CityData = CityData.append(Citydf, ignore_index=True)
CityData['UpdateTime'] = str(datetime.now())
CityData = CityData[['provinceName', 'cityName', 'currentConfirmedCount', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'locationId', 'UpdateTime']]  # 重排列顺序
filename = directory + UpdateTime + '_ChinaCity_Realtime.csv'
CityData.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# 中国省、直辖市、自治区实时数据
for dictt in data3:
    dictt.pop('cities')  # 删除城市数据
df = pd.DataFrame(data3)
df['UpdateTime'] = str(datetime.now())
filename = directory + UpdateTime + '_ChinaProvince_Realtime.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

base_dir = directory + 'chinaProvinceHistory/'
if not os.path.exists(base_dir):
    os.mkdir(base_dir)
# 中国省、直辖市、自治区历史数据
for dictt in data3:
    url = dictt['statisticsData']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    dailydata = requests.get(url=url, headers=headers).json()['data']
    df = pd.DataFrame(dailydata)
    df['provinceName'] = dictt['provinceName']
    filename = base_dir + dictt['provinceName'] + UpdateTime + '_history.csv'
    df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)


# 全球总量实时数据(分为包括中国的和不包括中国的全球数据)
# 13位时间戳转换为字符串日期
data8['createTime'] = datetime.fromtimestamp(data8['createTime'] / 1000).strftime("%Y-%m-%d %H:%M:%S")
data8['modifyTime'] = datetime.fromtimestamp(data8['modifyTime'] / 1000).strftime("%Y-%m-%d %H:%M:%S")
dd = {}
for i in ['foreignStatistics', 'globalStatistics']:
    dd[i] = data8[i]
    dd[i]['createTime'] = data8['createTime']
    dd[i]['modifyTime'] = data8['modifyTime']
df = pd.DataFrame(dd)
filename = directory + UpdateTime + '_globalTotal_Realtime.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig")

# 全球总量历史数据(不含中国)
url = data8['globalOtherTrendChartData']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
globalTotal = requests.get(url=url, headers=headers).json()['data']
df = pd.DataFrame(globalTotal)
filename = directory + UpdateTime + '_globalTotal_history.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)


# 保存当日最新国际新闻
for item in data2:
    # 13位时间戳转换为字符串日期
    for key in item.keys():
        if key in ['pubDate', 'createTime', 'modifyTime', 'dataInfoTime']:
            item[key] = datetime.fromtimestamp(item[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
df = pd.DataFrame(data2)
filename = directory + UpdateTime + '_InternationalNews.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# WHO文章
# 13位时间戳转换为字符串日期
for key in data4.keys():
    if key in ['createTime', 'modifyTime']:
        data4[key] = datetime.fromtimestamp(data4[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
df = pd.DataFrame(data4, index=[1])
# 将data4转换成数据框的另一种方式如下：
# s = pd.Series(data4)
# df = s.reset_index()
filename = directory + UpdateTime + '_WHOArticle.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# data5是图片，可以不用保存

# 建议和指导
for item in data6:
    # 13位时间戳转换为字符串日期
    for key in item.keys():
        if key in ['createTime', 'modifyTime']:
            item[key] = datetime.fromtimestamp(item[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
df = pd.DataFrame(data6)
filename = directory + UpdateTime + '_RecommendList.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# 辟谣
df = pd.DataFrame(data7)
filename = directory + UpdateTime + '_RumorList.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# 实时新闻播报(只能爬到最新几条)
for item in data9:
    # 13位时间戳转换为字符串日期
    for key in item.keys():
        if key in ['pubDate', 'createTime', 'modifyTime', 'dataInfoTime']:
            item[key] = datetime.fromtimestamp(item[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
df = pd.DataFrame(data9)
filename = directory + UpdateTime + '_WeiboNews.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

# 疾病知识
df = pd.DataFrame(data10['result'])
filename = directory + UpdateTime + '_knowledge.csv'
df.to_csv(filename, mode="w", encoding="utf_8_sig", index=False)

