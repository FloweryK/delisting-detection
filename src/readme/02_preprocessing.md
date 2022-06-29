# Delisting detection using W2V (Korean)

기업의 상장 폐지 여부를 네이버 뉴스와 신경망을 이용해 판단하는 프로젝트입니다. 



## Table of Contents

1. 데이터 수집: 기업명으로 검색한 네이버 뉴스 수집하기
2. 데이터 전처리: 데이터 클렌징하기, Word2Vec 훈련하기
3. 모델 훈련하기
4. 테스터, 요약본 시각화 자료 만들기



## 2. 데이터 전처리: 데이터 클렌징하기, Word2Vec 훈련하기

#### 관련 코드

`preprocessing.py` : 데이터 클렌징, 형태소 분석(mecab)
`word2vec.py`: 전처리 데이터 임베딩



#### Input과 Output

| 타입   | 설명                                                    | 파일                                                         |
| ------ | ------------------------------------------------------- | ------------------------------------------------------------ |
| Input  | 기업별 - 월별 뉴스 데이터 (제목, 날짜, 본문)            | `data/crawled/{기업명}/{기업명}_{시작날짜}_{끝날짜}.xlsx`    |
| Output | 기업마다 월별 뉴스 데이터 (제목, 날짜, 본문) (전처리됨) | `data/preprocessed/{기업명}/{기업명}_{시작날짜}_{끝날짜}.pickle` |



#### 실행방법

```bash
$ python preprocessing.py

====== DATA INFO ======
start : delisted/{company}, count : 0
...
start : listed/{company}, count : ~

$ python word2vec.py
====== DATA INFO ======
start : delisted/{company}
...
start : listed/{company}
...

```



## Installing Mecab

#### Mecab 설치방법(리눅스 서버 이용, 윈도우x)

파이썬의 형태소 분석기 패키지인 konlpy를 사용할 수 있도록 konlpy와 mecab을 설치.

**1. JDK 설치**

```bash
$ sudo apt-get install openjdk-8-jdk python-dev python3-dev
```

```
$ java -version
openjdk version "1.8.0_191"
OpenJDK Runtime Environment (build 1.8.0_191-8u191-b12-2ubuntu0.18.04.1-b12)
OpenJDK 64-Bit Server VM (build 25.191-b12, mixed mode)
```

**2. KoNLPy 설치**

```
$ pip install JPype1
$ pip install konlpy
```

**3. Mecab 설치** 

(최신다운로드 페이지 최신 다운로드 페이지 https://bitbucket.org/eunjeon/mecab-ko/downloads/)

```
$ wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
$ tar -zxvf mecab-*-ko-*.tar.gz
$ cd mecab-*-ko-*
$ ./configure
$ make
$ make check
$ sudo make install
```

**3-1. Mecab 버전확인**

```
$ mecab --version

아래와 같은 에러 발생 시
// mecab: error while loading shared libraries: libmecab.so.2: cannot open shared object file: 

다음의 명령을 입력 후 버전 재 확인
$ sudo ldconfig
$ ldconfig -p | grep /usr/local/lib
	libmecab.so.2 (libc6,x86-64) => /usr/local/lib/libmecab.so.2
	libmecab.so (libc6,x86-64) => /usr/local/lib/libmecab.so
```

**4. mecab-ko 설치**

```
$ wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz
$ tar -zxvf mecab-ko-dic-2.0.1-20150920.tar.gz
$ cd mecab-ko-dic-2.0.1-20150920/
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install

$ git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
$ cd mecab-python-0.996/
$ python3 setup.py build
$ python3 setup.py install
```

**5. Mecab 설치 테스트**

mecab -d /usr/local/lib/mecab/dic/mecab-ko-dic

아버지가 방에 들어가신다



![img](https://t1.daumcdn.net/cfile/tistory/99F247505C4862DD34)



![img](https://t1.daumcdn.net/cfile/tistory/99B59E505C4862DE12)











