# Delisting detection using W2V (Korean)

기업의 상장 폐지 여부를 네이버 뉴스와 신경망을 이용해 판단하는 프로젝트입니다. 



## Table of Contents

1. [데이터 수집: 기업명으로 검색한 네이버 뉴스 수집하기](src/readme/01_crawling.md)
2. [데이터 전처리: 데이터 클렌징하기, Word2Vec 훈련하기](src/readme/02_preprocessing.md)
5. [모델 훈련하기](src/readme/03_training.md)
6. 테스터, 요약본 시각화 자료 만들기



## Before we start

* 이 레포지토리의 코드들은 모두 python3, torch를 사용합니다. python3.6.8 이상을 사용하시는 걸 추천합니다. 



## Installing

1. 우선 다음을 통해 프로젝트를 가져오도록 합니다.

   ```bash
   $ git clone https://github.com/Tmax-AI3-3/delisting_detection.git
   ```

2. (옵션: 가상환경 사용하기)  다음을 통해 가상환경을 만들어 프로젝트 내에서만 사용하는 라이브러리들을 관리할 수 있습니다.
   
```bash
   $ virtualenv venv -p python3
   $ source venv/bin/activate # 가상환경 켜기 (linux, mac)
   $ source venv/Scripts/activate # 가상환경 켜기 (Windows)
   $ deactivate # 가상환경 끄기
```

3. 필요한 라이브러리들을 설치합니다.  (torch는 `requirements.txt`가 제대로 입력되지 않는 경우가 많아, 직접 설치하는 것을 권장합니다: https://pytorch.org/)

   ```bash
   $ pip3 install -r requirements.txt
   ```

   

## How to run the codes

코드의 설명과 작동 방식은 각 디렉토리 내 README.md에서 설명합니다. 



## Pipeline

| 순서 | 실행 파일                | 생성 파일                                                    |
| ---- | ------------------------ | ------------------------------------------------------------ |
| 1    | -                        | `src/listed_list_2020.07.01.xlsx`                            |
| 2    | `data_crawler_listed.py` | `data/crawled/{기업명}/{기업명}_{시작날짜}_{끝날짜}.xlsx`    |
| 3    | `preprocessing.py`       | `data/preprocessed/{기업명}/{기업명}_{시작날짜}_{끝날짜}.pickle` |
| 4    | `tester.py`              | `data/tested/{%Y-%m-%d_%H-%M-%S}_{W2V_MODEL_NAME}/trial_{#}.json` |





## Troubleshooting

##### [Windows] import torch 에러 (DLL load failed, WinError 126)

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
  ...
    self._handle = _dlopen(self._name, mode)
OSError: [WinError 126] The specified module could not be found
```

윈도우 환경에서 윈도우 업데이트가 제대로 되지 않은 경우 발생하는 에러입니다. Process Monitor로 확인하면, MSVCP140.dll을 찾을 수 없어 로드하지 못하는 것을 알 수 있습니다. 

마이크로소프트 공식 홈페이지 [Visual Studio 2015용 Visual C++ 재배포 가능 패키지](https://www.microsoft.com/ko-kr/download/details.aspx?id=48145)에서 파일을 다운받아 설치하시면 정상적으로 로드 할 수 있습니다. 



