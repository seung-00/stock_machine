import requests
from bs4 import BeautifulSoup
import random
import pandas as pd

import re
from tensorflow.keras.models import load_model
import predict
model = load_model('./Model2020_08_28_00시20분23초.h5')
def date_cleansing(test):
        date_text=[]
        try:
            #지난 뉴스
            #머니투데이 10면1단 2018.11.05. 네이버뉴스 보내기
            pattern = '\d+.(\d+).(\d+).' #정규표현식
            r = re.compile(pattern)
            match = r.search(test).group(0) # 2018.11.05.
            date_text.append(match)
            return date_text[0]

        except AttributeError:
            #최근 뉴스
            #이데일리 1시간 전 네이버뉴스 보내기
            pattern = '\w* (\d\w*)' #정규표현식
            r = re.compile(pattern)
            match = r.search(test).group(1)
            #print(match)
            date_text.append(match)
            return date_text[0]
def get_newses(keyword):
    f = open("navernews.csv", "w")
    # 데이터의 헤더부분을 입력한다.
    f.write("headline, label, date\n")
    number = 0
    page = 1
    for page in range(1, 10000,10):
        raw = requests.get("https://search.naver.com/search.naver?where=news&query="+keyword+"&start=" + str(page),
                           headers={"User-Agent": "Mozilla/5.0"})
        html = BeautifulSoup(raw.text, 'html.parser')
        # 컨테이너: ul.type01 > li
        # 기사제목: a._sp_each_title
        # 언론사: span._sp_each_source
        articles = html.select("ul.type01 > li")
        for ar in articles:
            L, R = [],[]
            title = ar.select_one("a._sp_each_title").text
            source = ar.select_one('.txt_inline').text
            L.append(title)
            R.append(source)
            number=number+1
            label = predict.classification(L,model)[0]
            title = title.replace(",", "")
            date = source.replace(",", "")
            date = date_cleansing(date)
            print('['+str(number)+']'+title+' ['+label+date+']')

            try:
                f.write(title+ ','+label+','+date+'\n')
            except:
                pass
    # navernews.csv 파일 닫음
    f.close()

def shuffle(filename):
    data = pd.read_csv(filename, encoding='CP949')
    x_train = []
    y_train = []
    for sentence in data['headline']:
        x_train.append(sentence)
    for sentence in data['label']:
        y_train.append(sentence)
    tmp = [[x, y] for x, y in zip(x_train, y_train)]
    random.shuffle(tmp)
    x_train = [n[0] for n in tmp]
    y_train = [n[1] for n in tmp]
    data = pd.DataFrame({
        'headline': x_train,
        'label': y_train
    })
    data.to_csv('result.csv', index=False, encoding='cp949')

if __name__ == '__main__':
    get_newses("삼성전자")
    #shuffle('Data/train.csv')
    #shuffle('Data/test.csv')