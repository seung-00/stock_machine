# selenium driver : C:\\Users\\user1\\Desktop\\StockNews\\chromedriver.exe
from selenium import webdriver
import datetime
import pandas as pd
import csv
import urllib.request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import time
Head = True
def PrintNews(headline_list, news_info, Text, CompanyFromNews):
    for i in range(len(headline_list)):
        print('|'+ news_info[i], end = '| ')
        print(headline_list[i], end=' / ')
        print("[기업정보 : "+CompanyFromNews[i]+"]")
        #print(Text[i]) #본문보기

def PrintPrice(NameList, PriceInfo, Fluctuation):
    for i in range(len(NameList)):
        print(NameList[i], end=' : ')
        print(PriceInfo[i], end='[KRW] / Fluctuation : ')
        print(Fluctuation[i])
def News_get_driver(Headless):
   if(Headless):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/root/StockNews/chromedriver",chrome_options=chrome_options)
        driver.implicitly_wait(1)
   else:
       driver = webdriver.Chrome("/root/StockNews/chromedriver")
   url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=258"  # Naver Stock News
   driver.get(url)  # driver open
   return driver

def GetNews(driver):
    headline_list = []
    news_info = []
    Text = []
    NewsUrl = []
    table = driver.find_element_by_class_name('type06_headline') # Section 1 Table 파싱
    rows = table.find_elements_by_tag_name("li")
    for index, value in enumerate(rows):
        try:
            body = value.find_elements_by_tag_name('dt')[1] #이미지가 첨부된 뉴스 헤드라인 파싱
            link = body.find_elements_by_tag_name('a')[0].get_attribute('href')
            NewsUrl.append(link)
            headline_list.append(body.text)
            info = value.find_elements_by_tag_name('dd')[0] # 신문사, 시간 파싱
        except:
            body = value.find_elements_by_tag_name('dt')[0] # 이미지 미첨부 뉴스 헤드라인 파싱
            link = body.find_elements_by_tag_name('a')[0].get_attribute('href')
            NewsUrl.append(link)
            headline_list.append(body.text)
        try:
            #//*[@id="main_content"]/div[2]/ul[1]/li[2]/dl/dt[2]/a
            info = value.find_elements_by_tag_name('dd')[0] # 신문사, 시간 파싱
            info = info.text.split("\n")
            news_info.append(info[1])
            Text.append(info[0])
        except:
            print("Err ] info parsing")

    table = driver.find_element_by_class_name('type06') # Section 2 Table
    rows = table.find_elements_by_tag_name("li")
    for index, value in enumerate(rows):
        try:
            body = value.find_elements_by_tag_name('dt')[1] #이미지가 첨부된 뉴스 헤드라인 파싱
            link = body.find_elements_by_tag_name('a')[0].get_attribute('href')
            NewsUrl.append(link)
            headline_list.append(body.text)
        except:
            body = value.find_elements_by_tag_name('dt')[0] # 이미지 미첨부 뉴스 헤드라인 파싱
            link = body.find_elements_by_tag_name('a')[0].get_attribute('href')
            NewsUrl.append(link)
            headline_list.append(body.text)
        try:
            info = value.find_elements_by_tag_name('dd')[0]  # 신문사, 시간 파싱
            info = info.text.split("\n")
            news_info.append(info[1])
            Text.append(info[0])
        except:
            print("Err ] info parsing")
            
    return headline_list, news_info, Text, NewsUrl # 순서대로 헤드라인, 신문사 정보 및 시간 정보, 본문 내용

def save_headlines(headline_list, news_info, Text,CompanyFromNews,NewsUrl):
    now = datetime.datetime.now()
    # print(now)  # 2015-04-19 12:11:32.669083
    #
    # nowDate = now.strftime('%Y-%m-%d')
    # print(nowDate)  # 2015-04-19
    #
    # nowTime = now.strftime('%H:%M:%S')
    # print(nowTime)  # 12:11:32
    nowDatetime = now.strftime('%Y_%m_%d_%H시%M분%S초')
    #print("[현재 시각] : " + nowDatetime)  # 2015-04-19 12:11:32

    data = pd.DataFrame({
        '헤드라인' : headline_list,
        '신문사 정보' : news_info,
        '본문' : Text,
        '기업정보' : CompanyFromNews,
        '기사 주소' : NewsUrl
    })
    data.to_csv('Data/News'+nowDatetime+'.csv', index = False, encoding='cp949')
    return 'Data/News'+nowDatetime+'.csv'

def NowPriceDriver(Headless):
    if (Headless):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/root/StockNews/chromedriver",
                                  chrome_options=chrome_options)
        driver.implicitly_wait(3)
    else:
        driver = webdriver.Chrome("/root/StockNews/chromedriver")
    url = "https://kr.investing.com/indices/south-korea-indices"  # 다음금융
    driver.get(url)  # driver open

    return driver

def get_prices(driver):
    NameList = ["KOSPI", "KOSDAQ"] # 종목
    PriceInfo=[] # 현재 가격 정보
    Fluctuation = [] #전일 대비 변동폭
    #table = driver.find_element_by_css_selector('body > div > div.body-wrap > div.info-first > div.section-wap-top')

    Kospi_price = driver.find_element_by_xpath('//*[@id="pair_37426"]/td[3]').text
    Kosdaq_price = driver.find_element_by_xpath('//*[@id="pair_38016"]/td[3]').text
    PriceInfo.append(Kospi_price)
    PriceInfo.append(Kosdaq_price)

    Kospi_Fluctuation = driver.find_element_by_xpath('/html/body/div[5]/section/table/tbody/tr/td/table/tbody/tr[2]/td[6]').text+"["+driver.find_element_by_xpath('/html/body/div[5]/section/table/tbody/tr/td/table/tbody/tr[2]/td[7]').text+"]"
    Kosdaq_Fluctuation = driver.find_element_by_xpath('/html/body/div[5]/section/table/tbody/tr/td/table/tbody/tr[10]/td[6]').text+"["+driver.find_element_by_xpath('/html/body/div[5]/section/table/tbody/tr/td/table/tbody/tr[10]/td[7]').text+"]"
    Fluctuation.append(Kospi_Fluctuation)
    Fluctuation.append(Kosdaq_Fluctuation)
    return NameList, PriceInfo, Fluctuation

def GetCompanyList():
   filepath = 'KospiList.txt' #코스피
   CompanyList = []
   with open(filepath, mode = 'rt', encoding='utf-8') as file:
       while True:
           company = file.readline()
           if not company: break
           CompanyList.append(company.split('\n')[0])
           
   filepath = 'Kosdaq.txt' #코스닥
   with open(filepath, mode='rt', encoding='utf-8') as file:
       while True:
           company = file.readline()
           if not company: break
           CompanyList.append(company.split('\n')[0])
   return CompanyList

def company_in_news(news,CompanyList):
    result = "None"
    for i in CompanyList:
        if (i in news): #한화, 한화투자운용 구분위함
            if(result =="None"):
                result = str(i)
            else:
                if(len(result)<len(str(i))):
                    result = str(i)
    return result

def GetCompanyFromNews(headlines, CompanyList):
    CompanyFromNews = []
    for news in headlines:
        Company = company_in_news(news,CompanyList)
        if(Company == "None"):
            CompanyFromNews.append('-')
        else:
            CompanyFromNews.append(Company)
    return CompanyFromNews

def MakeCompanyCSV():
    filepath = 'KospiList.txt'  # 코스피
    CompanyList = []
    with open(filepath, mode='rt', encoding='utf-8') as file:
        while True:
            company = file.readline()
            if not company: break
            CompanyList.append(company.split('\n')[0])

    filepath = 'Kosdaq.txt'  # 코스닥
    with open(filepath, mode='rt', encoding='utf-8') as file:
        while True:
            company = file.readline()
            if not company: break
            CompanyList.append(company.split('\n')[0])
    number = range(1,len(CompanyList)+1)
    data = pd.DataFrame({
        '번호': number,
        '기업명' : CompanyList,
        '뉴스' : ['']*len(CompanyList)
    })
    data.to_csv('Data/CompanyNewsList.csv', index=False, encoding='cp949')

def FindWritePoint(line):
    write_point = 0
    for i in range(len(line)):  # write할 위치 찾기
        if (line[i] == ''):
            write_point = i
            return write_point
    return write_point

def Write_News(headlines, CompanyFromNews,nowDatetime):
    file = open('Data/CompanyNewsList.csv', 'r', encoding='euc-kr')
    reader = csv.reader(file)
    lines=[]
    NewsFile = []
    write_point=0
    for line in reader:
        write_point = FindWritePoint(line)
        for index in range(len(CompanyFromNews)):
            if (line[1] == CompanyFromNews[index]):
                line[write_point] = str('[#]')+nowDatetime+str('[#]')+headlines[index]
                NewsFile.append(CompanyFromNews[index] + " : "+headlines[index])
        lines.append(line)
    file = open('Data/CompanyNewsList.csv', 'w', newline='', encoding='euc-kr')
    writer = csv.writer(file)
    writer.writerows(lines)
    file.close()
    # print("#기업별 뉴스 CSV File 작성 완료")
    return NewsFile
def Get_KospiGraphDriver(Headless):
    if (Headless):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/root/StockNews/chromedriver",
                                  chrome_options=chrome_options)
        driver.implicitly_wait(3)
    else:
        driver = webdriver.Chrome("/root/StockNews/chromedriver")
    url = "https://finance.daum.net/"  # 다음금융
    driver.get(url)  # driver open
    return driver

def GetKospiGraph(driver, PriceInfo, Fluctuation ):
    # KTOP 30, KOSPI, KOSPI200, KOSDAQ, KOSDAQ150, KRX300 순
    KospiImg = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div[1]/a/img')
    KosdaqImg = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div[2]/a/img')
    link=KospiImg.get_attribute('src')
    urllib.request.urlretrieve(link, '../Frontend/client/src/img/Kospi.jpg') #코스피 이미지 다운로드
    link=KosdaqImg.get_attribute('src')
    urllib.request.urlretrieve(link, '../Frontend/client/src/img/Kosdaq.jpg') #코스닥 이미지 다운로드
    time.sleep(5)
    KospiGraph =  Image.open("../Frontend/client/src/img/Kospi.jpg").convert("RGBA")
    KosdaqGraph = Image.open("../Frontend/client/src/img/Kosdaq.jpg").convert("RGBA")

    fig = plt.figure(figsize=(16,6))
    rows = 1
    cols = 2
    ax1 = fig.add_subplot(rows, cols, 1)
    ax1.imshow(KospiGraph)
    ax1.set_xlabel('KOSPI\nPrice : '+PriceInfo[0]+' / Fluctuation : '+Fluctuation[0])
    ax1.set_xticks([]), ax1.set_yticks([])

    ax2 = fig.add_subplot(rows, cols, 2)
    ax2.imshow(KosdaqGraph)
    ax2.set_xlabel('KODAQ\nPrice : '+PriceInfo[1]+' / Fluctuation : '+Fluctuation[1])
    ax2.set_xticks([]), ax2.set_yticks([])
    plt.savefig('./KOSPI_KOSDAQ.png')

    plt.close(fig)
    fname = "KOSPI_KOSDAQ.png"
    TRANSPERENT = False
    if(TRANSPERENT):
        img = Image.open(fname)
        img = img.convert("RGBA")

        datas = img.getdata()
        newData = []
        for item in datas:
            if (item[0] == 255 and item[1] == 255 and item[2] == 255):  # 해당 픽셀 색이 흰색이면
                newData.append((255, 255, 255, 0))  # 투명 추가
            else:
                newData.append(item)
        img.putdata(newData)  # 데이터 입력
        img.save(fname)  # 이미지name으로 저장