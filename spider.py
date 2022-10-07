from cmath import log
from email.mime import base
from time import time
from urllib import response
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request
import urllib.error
import xlwt  # 进行excel操作
import sqlite3  # 进行 SQLite 数据库操作

findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findName = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

def main():
    baseUrl = 'https://movie.douban.com/top250?start=0'

    # 1. 爬取网页
    dataList = getData(baseUrl)

    savePath = ".\\豆瓣电影Top250.xls"

    saveData(savePath, dataList)

    # askUrl(baseUrl)

def getData(baseUrl):
    dataList = []
    dataList.append(['电影网址', '电影图片网址', '电影中文名', '电影外国名', '评分', '点评数量', '概况', '相关信息'])

    for i in range(0, 1):
      url = baseUrl + str(i * 25)
      html = askUrl(url)

      # 逐一解析网页
      bs = BeautifulSoup(html, "html.parser")
      for item in bs.find_all('div', class_="item"):
        # print('item是这个：', item)
        data = []   # 保存一部电影的所有信息
        item = str(item)

        link = re.findall(findLink, item)[0]
        data.append(link)

        imgLink = re.findall(findImgSrc, item)[0]
        data.append(imgLink)

        name = re.findall(findName, item)
        if(len(name) == 2) :
          cName = name[0]
          data.append(cName)
          oName = name[1].replace("/", "")
          data.append(oName)
        else:
          data.append(name[0])
          data.append(' ')

        rating = re.findall(findRating, item)[0]
        data.append(rating)

        judge = re.findall(findJudge, item)[0]
        data.append(judge)

        inq = re.findall(findInq, item)
        if len(inq) != 0 :
          inq = inq[0].replace("。", "")
          data.append(inq)
        else:
          data.append(" ")

        bd = re.findall(findBd, item)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
        bd = re.sub('/', " ", bd)
        data.append(bd.strip())

        dataList.append(data)

    return dataList


def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as err:
        if hasattr(err, 'code'):
            print(err.code)
        if hasattr(err, 'reason'):
            print(err.reason)
            
    return html

def saveData(savePath, dataList):
  workbook = xlwt.Workbook(encoding="utf-8")
  workSheet = workbook.add_sheet('sheet1')

  for index in range(len(dataList)):
    for jndex in range(len(dataList[index])): 
      workSheet.write(index, jndex, dataList[index][jndex])

  workbook.save(savePath)


if __name__ == '__main__':
    main()
