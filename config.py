import datetime

# dataset.py
PROC_DIR = 'data/preprocessed'
CACHE_DIR = 'cache/dataset'
CACHE_MODEL_DIR = 'cache/w2v_models'
W2V_MODEL_PATH = 'cache/model.w2v'
FILTERS = ['코스닥시장 이전상장', '코스닥시장 상장', '유가증권시장 상장', '완전자회사화', '해산 사유 발생']
LIMIT = 100

# trainer.py
R_TRAIN = 0.8
R_TEST = 0.2
R_VALI = 0
N_HIDDEN = 256
N_EPOCH = 500

# tester.py
TEST_DIR = 'data/tested' + '/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_' + W2V_MODEL_PATH.split('/')[-1]
N_TEST = 100

# summary.py
TEST_ROOT = 'data/tested/' + '2020-07-14_16-44-19_model_wiki.w2v'
SUMMARY_DIR = 'data/summary'