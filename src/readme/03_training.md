# Delisting detection using W2V (Korean)

기업의 상장 폐지 여부를 네이버 뉴스와 신경망을 이용해 판단하는 프로젝트입니다. 



## Table of Contents

1. 데이터 수집: 기업명으로 검색한 네이버 뉴스 수집하기
2. 데이터 전처리: 데이터 클렌징하기, Word2Vec 훈련하기
5. 모델 훈련하기
6. 요약본 시각화 자료 만들기



## 3. 모델 훈련하기

#### 관련 코드

`dataset.py` : dataset class 생성
`model.py`: 신경망 구성
`trainer.py`: 신경망을 훈련하는 부분
`tester.py`: 원하는 Trial만큼 `trainer.py`에서 Test를 진행하는 부분



#### Input과 Output

| 타입   | 설명                                                         | 파일                                                         |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Input  | 기업마다 월별 뉴스 데이터 (제목, 날짜, 본문) (전처리됨)      | `data/preprocessed/{기업명}/{기업명}_{시작날짜}_{끝날짜}.pickle` |
| Output | 타겟 기업, {epoch, train loss, test loss, confusion matrix, precision, recall, f1, accuracy, error} | `data/tested/{%Y-%m-%d_%H-%M-%S}_{W2V_MODEL_NAME}/trial_{#}.json` |



#### 실행방법

```bash
$ python tester.py
```

