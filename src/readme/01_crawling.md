# Delisting detection using W2V (Korean)

기업의 상장 폐지 여부를 네이버 뉴스와 신경망을 이용해 판단하는 프로젝트입니다. 



## Table of Contents

1. 데이터 수집: 기업명으로 검색한 네이버 뉴스 수집하기
2. 데이터 전처리: 데이터 클렌징하기, Word2Vec 훈련하기
5. 모델 훈련하기
6. 테스터, 요약본 시각화 자료 만들기



## 1. 데이터 수집

#### 관련 코드

`query_crawler.py` : 쿼리 기반 네이버 뉴스 크롤러 (실제 크롤링를 하는 부분)
`data_crawler_listed.py`: 상장 중 기업명을 쿼리로 `query_crawler.py` 에게 수집하게 하는 부분
`data_crawler_delisted.py` : 상장 폐지 기업명을 쿼리로 `query_crawler.py` 에게 수집하게 하는 부분

※ `data_crawler_delisted.py`와 `data_crawler_listed.py`는 작동방식이 같으므로 하나만 설명합니다. 



#### Input과 Output

| 타입   | 설명                                         | 파일                              |
| ------ | -------------------------------------------- | --------------------------------- |
| Input  | 상장 중 기업 리스트                          | `src/listed_list_2020.07.01.xlsx` |
| Output | 기업별 - 월별 뉴스 데이터 (제목, 날짜, 본문) | ㅇㅁ                              |



#### 실행방법

```bash
$ python data_crawler_listed.py

====== DATA INFO ======
2020-07-30 11:32:41.135292
name: 3S 0 / 2352

start crawling: 3S from 2020.06.01 to 2020.06.25

crawling... 3S (page 1/1)
opening url: https://search.naver.com/search.naver?&where=news&query=3S&sort=0&field=1&ds=2020.06.01&de=2020.06.25&nso=so:r,p:from20200601to20200625&start=1&refresh_start=0
parsing html
        opening inside https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=018&aid=0004665862
        opening inside https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=015&aid=0004361436
        
...
```

크롤링을 도중에 멈추었다가 다시 시작할 경우, 만약 타겟 기간을 이미 수집한 결과가 있다면 건너뛰게 됩니다.

```bash
$ python data_crawler_listed.py

====== DATA INFO ======
2020-07-30 11:36:19.596019
name: 3S 0 / 2352

start crawling: 3S from 2020.06.01 to 2020.06.25
already crawled. go to next step

...
```



#### 실행 결과

수집된 결과는 `CRAWL_DIR/{기업명}` 디렉토리마다  `{기업명}_{시작날짜}_{끝날짜}.xlsx` 파일들로 저장됩니다. 내용물은 다음과 같은 형태를 가집니다:

![003_dataset_01](01_crawling_01.PNG)



