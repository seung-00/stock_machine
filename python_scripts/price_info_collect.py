import urllib
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlrd
import pandas as pd
import pymysql
import DBHandler
host = 'db-4q5u4.pub-cdb.ntruss.com'
ID= 'stockadmin'
PW='interface123!@#'
DB_name='stock'
def find_price(code): #50일 자료 fetch
    stockItem = code
    url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockItem
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    maxPage = source.find_all("table", align="center")
    mp = maxPage[0].find_all("td", class_="pgRR")
    Date=[]
    end_price=[]
    start_price=[]
    highest=[]
    lowest=[]
    volume=[]
    mpNum = 5 #Max Page
    for page in range(1, mpNum + 1):
        url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockItem + '&page=' + str(page)
        html = urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        srlists = source.find_all("tr")
        isCheckNone = None

        if ((page % 1) == 0):
            time.sleep(0.2)
        for i in range(1, len(srlists) - 1):
            if (srlists[i].span != isCheckNone):
                srlists[i].td.text
                Date.append(srlists[i].find_all("td", align="center")[0].text)
                end_price.append(srlists[i].find_all("td", class_="num")[0].text) #종가
                start_price.append(srlists[i].find_all("td", class_="num")[2].text) #시가
                highest.append(srlists[i].find_all("td", class_="num")[3].text)  # 고가
                lowest.append(srlists[i].find_all("td", class_="num")[4].text)  # 저가
                volume.append(srlists[i].find_all("td", class_="num")[5].text)
                # print(srlists[i].find_all("td", align="center")[0].text, srlists[i].find_all("td", class_="num")[0].text,srlists[i].find_all("td", class_="num")[5].text)
    return Date,end_price, start_price, highest, lowest,volume
def getTodayPrice(code):
    stockItem = code
    url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockItem
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    maxPage = source.find_all("table", align="center")
    mp = maxPage[0].find_all("td", class_="pgRR")
    Date = []
    end_price = []
    start_price = []
    highest = []
    lowest = []
    volume = []
    mpNum = 1  # Max Page
    for page in range(1, mpNum + 1):
        url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockItem + '&page=' + str(page)
        html = urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        srlists = source.find_all("tr")
        isCheckNone = None

        if ((page % 1) == 0):
            time.sleep(0.2)
        for i in range(2, 3):
            if (srlists[i].span != isCheckNone):
                srlists[i].td.text
                Date.append(srlists[i].find_all("td", align="center")[0].text)
                end_price.append(srlists[i].find_all("td", class_="num")[0].text)  # 종가
                start_price.append(srlists[i].find_all("td", class_="num")[2].text)  # 시가
                highest.append(srlists[i].find_all("td", class_="num")[3].text)  # 고가
                lowest.append(srlists[i].find_all("td", class_="num")[4].text)  # 저가
                volume.append(srlists[i].find_all("td", class_="num")[5].text)
                #print(srlists[i].find_all("td", align="center")[0].text, srlists[i].find_all("td", class_="num")[0].text,srlists[i].find_all("td", class_="num")[5].text)
    print(Date[0], end_price[0], start_price[0], highest[0], lowest[0], volume[0])
    return Date[0], end_price[0], start_price[0], highest[0], lowest[0], volume[0]

def generate_codeInsert_query():
    xlsx = xlrd.open_workbook('Data/stockdata.xls')
    sheet = xlsx.sheet_by_index(0)
    for i in range(1,101):
        code = sheet.cell(i, 0).value
        stock = sheet.cell(i,1).value
        print("INSERT INTO `stock`.`pricelist` (`code`, `company`) VALUES ('info_"+code+"', '"+stock+"');")

def generate_newsInsertQuery():
    xlsx = xlrd.open_workbook('Data/News.xlsx')
    DBController = DBHandler.MySqlController(host, ID, PW, DB_name)
    sheet = xlsx.sheet_by_index(0)
    for i in range(1, 2049):
        company = sheet.cell(i, 0).value
        headline = sheet.cell(i, 1).value
        Text = sheet.cell(i, 2).value
        URL = sheet.cell(i, 3).value
        NewsInfo = sheet.cell(i, 4).value
        Time = sheet.cell(i, 5).value
        print(headline)
        sql = "INSERT IGNORE INTO NewsHistory VALUES(%s, %s, %s, %s, %s, %s)"
        DBController.curs.execute(sql, (company, headline, Text, URL, NewsInfo, Time))
        DBController.conn.commit()


def return_code(company):
    xlsx = xlrd.open_workbook('Data/stockdata.xls')
    sheet = xlsx.sheet_by_index(0)
    for i in range(1, 101):
        code = sheet.cell(i, 0).value
        stock = sheet.cell(i, 1).value
        if(stock == company):
            return code
    return "None"
def write_history(company):
    code = return_code(company)
    if(code=="None"):
        return
    else:
        Date,end_price, start_price, highest, lowest,volume = find_price(code)
        data = pd.DataFrame({
            '날짜': Date,
            '종가': end_price,
            '시가': start_price,
            '고가' : highest,
            '저가' : lowest,
            '거래량': volume
        })
        data.to_csv('Data/Histories/'+company+'_Info.csv', index=False, encoding='cp949')
        print(company+" Done.")
def Update_TodayPrice_info(): #오늘 가격정보 추가 주식시장이 종료된 경우만 해주셈
    DBController = DBHandler.MySqlController(host, ID, PW, DB_name)
    xlsx = xlrd.open_workbook('Data/stockdata.xls')
    sheet = xlsx.sheet_by_index(0)
    for i in range(1, 101):
        code = sheet.cell(i, 0).value
        stock = sheet.cell(i, 1).value
        Date, end_price, start_price, highest, lowest, volume = getTodayPrice(code)
        DBController.UpdateTodayPrice(stock,Date, end_price, start_price, highest, lowest, volume)

if __name__ == '__main__':
       #xlsx = xlrd.open_workbook('Data/stockdata.xls')
       #sheet = xlsx.sheet_by_index(0)
       #for i in range(1, 101):
       #     code = sheet.cell(i, 0).value
       #     stock = sheet.cell(i, 1).value
       #     write_history(stock)
      #Update_Price_info()
      #DBController = DBHandler.MySqlController(host, ID, PW, DB_name)
      #DBController.UpdatePrice()
      while(True):
          Update_TodayPrice_info()
          time.sleep(30)
      #generate_newsInsertQuery()
      #generate_codeInsert_query()


