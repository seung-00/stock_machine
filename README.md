# Stock news analysis web

종목의 주가 상승, 하락을 예측하는 웹 서비스입니다.

기본적 분석에 사용되는 경제 지표들과 실시간으로 경제 뉴스를 파싱해 기업별 호재, 악재를 분류한 데이터를 추가로 학습해 종목을 분석했습니다.

---

주요 프레임워크, 라이브러리

* Selenium, Beautiful-Soup, Tensorflow, Spring Boot, React.js

모델

* LSTM 기반으로 특정 종목에 대한 증권 뉴스를 호재, 악재, 중립으로 분류
* Logistic Regression 기반으로 주가 상승/하락 학습 및 예측

데이터

* 한국거래소에서 파싱해온 20년 분량 KOSPI 100대 기업의 종목정보(종가, 등락폭, PBR 등)
* 네이버 증권뉴스