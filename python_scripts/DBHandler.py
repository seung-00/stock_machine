# Data/Kosdaq.jpg
# Data/Kospi.jpg
# Data/News ~ .csv
# Data/CompanyNewsList.csv
import pymysql
import xlrd
import pandas as pd
import numpy as np
class MySqlController:
    def __init__(self, host, id, pw, db_name):

        self.conn = pymysql.connect(host = host, user = id, password = pw, db = db_name, charset='utf8')
        self.curs = self.conn.cursor()

    def UpdateNews(self, CompanyFromNews, Headline, Text, URL, NewsInfo,label):
        for index in range(0,len(CompanyFromNews)):
            sql = 'UPDATE News SET Company = %s, Headline = %s, Text = %s, URL = %s, Info = %s, Label = %s where IDX = %s'
            self.curs.execute(sql, (CompanyFromNews[index], Headline[index], Text[index], URL[index], NewsInfo[index], label[index], str(index+1)))
            self.conn.commit()
        print("Stock News Updated.")
    def InsertNewsHistory(self, CompanyFromNews, Headline, Text, URL, NewsInfo,DateTime):
        for index in range(0,len(CompanyFromNews)):
            sql = 'Insert IGNORE  INTO NewsHistory VALUES(%s, %s, %s, %s, %s,%s)'
            self.curs.execute(sql, (CompanyFromNews[index], Headline[index], Text[index], URL[index], NewsInfo[index], DateTime))
            self.conn.commit()
        print("Stock NewsHistory Updated.")
    def UpdatePrice(self):
        xlsx = xlrd.open_workbook('Data/stockdata.xls')
        sheet = xlsx.sheet_by_index(0)
        for i in range(1, 101):
            code = sheet.cell(i, 0).value
            stock = sheet.cell(i, 1).value
            for j in range(1, 50):
                info_csv = pd.read_csv('Data/Histories/' + stock + '_info.csv', encoding='CP949')
                date = info_csv.iloc[j][0]
                end_price = info_csv.iloc[j][1]
                start_price = info_csv.iloc[j][2]
                highest = info_csv.iloc[j][3]
                lowest = info_csv.iloc[j][4]
                volume = info_csv.iloc[j][5]
                sql = "INSERT IGNORE INTO pricelist VALUES(%s, %s, %s, %s, %s, %s, %s)"
                print(stock, date, end_price, start_price, highest, lowest,volume)
                self.curs.execute(sql, (stock,date, end_price, start_price, highest, lowest,volume))
                self.conn.commit()
    def UpdateTodayPrice(self,stock, Date,end_price, start_price, highest, lowest,volume):
        '''
        INSERT INTO pricelist VALUES('삼성전자', '2020-09-18', '59,400', '59,900','59,900','59,900','59,900')
ON DUPLICATE KEY UPDATE endprice='59,400', startprice='59,400',highest='59,400',lowest='59,400',volume ='59,400';
        '''
        sql = "INSERT INTO pricelist VALUES(%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE endprice=%s, startprice=%s,highest=%s,lowest=%s,volume =%s"

        self.curs.execute(sql, (stock,Date, end_price, start_price, highest, lowest,volume,end_price, start_price, highest, lowest,volume))
        self.conn.commit()

    def CreateTable(self):
        xlsx = xlrd.open_workbook('Data/stockdata.xls')
        sheet = xlsx.sheet_by_index(0)
        for i in range(1, 101):
            code = sheet.cell(i, 0).value
            stock = sheet.cell(i, 1).value
            sql = 'CREATE TABLE info_'+code+' (DATE_INFO DATE NOT NULL, END_PRICE VARCHAR(20) NOT NULL, START_PRICE VARCHAR(20) NOT NULL, HIGHEST VARCHAR(20) NOT NULL,LOWEST VARCHAR(20) NOT NULL, VOLUME VARCHAR(30), UNIQUE (DATE_INFO));'
            self.curs.execute(sql)
            self.conn.commit()
    def update_totalprice(self, PriceList, Fluctuation):
        sql = "UPDATE TotalPrice SET Price = %s, Fluctuation = %s where name = 'KOSPI'"
        self.curs.execute(sql, (PriceList[0], Fluctuation[0]))
        self.conn.commit()
        sql = "UPDATE TotalPrice SET Price = %s, Fluctuation = %s where name = 'KOSDAQ'"
        self.curs.execute(sql, (PriceList[1], Fluctuation[1]))
        self.conn.commit()

    def update_predict_result(self, price, volume, div, bps, per, eps, pbr, model_result,score, result,code):
        sql = "UPDATE Top100 SET Prices = %s,Volumes = %s,DIVs = %s,BPS = %s,PER = %s,EPS = %s,PBR = %s,model1 = %s,model2 = %s, result = %s WHERE Codes = %s"
        self.curs.connection.encoders[np.int64] = lambda value, encoders: int(value)
        self.curs.execute(sql, (price, volume, div, bps, per, eps, pbr, model_result,score, result, code))
        self.conn.commit()
    def get_newses(self, company):
        sql = "SELECT * FROM NewsHistory where Company = %s"
        self.curs.execute(sql, (company))
        self.conn.commit()
        result = self.curs.fetchall()
        Headlines = []
        for row_data in result:
            Headline = row_data[1]
            Headlines.append(Headline)
        return Headlines