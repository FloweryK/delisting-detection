"""
By Youngjin Kim,
Edited By Minsang Yu, flowerk94@gmail.com
"""

import os
import re
import nltk
nltk.download('punkt')
import mecab
import argparse
import pandas as pd
from tqdm import tqdm
# pd.options.display.max_columns = None
# pd.options.display.max_rows = None
from multiprocessing import Pool
import utils


def cleaning(text):
    # ??
    text = text.replace('\\\\n ', '').replace('\\t', '').replace('fnRASSI', '')

    # html 제거
    text = re.sub('<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>', '', text)
    text = re.sub('<[^>]*>', ' ', text)

    # url 제거
    text = re.sub('https?://(\w*:\w*@)?[-\w.]+(:\d+)?(/([\w/_.]*(\?\S+)?)?)?', '', text)

    # ??
    text = re.sub('w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)

    # ??
    text = re.sub('((\w+:\/\/\S+)|(\w+[\.:]\w+\S+))[^\s,\.]*', '', text)

    # 이메일 제거
    text = re.sub('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', '', text)

    # 전화번호 제거
    text = re.sub('\d\d\d-\d\d\d-\d\d\d\d', '', text)

    # 특수문자 제거
    text = re.sub('[-=+#/\?:^$@*\"\n\t※~‘‘＜＞☞★&ㆍ◆△◇ㅁ!↑』←▲ⓒ""▶·“”《‥\\\\\(\)\[\]\<\>`\'…》]', ' ', text)

    return text


def extract_only_stems(sentence):
    # mecab
    me = mecab.MeCab()

    # filters
    FILTERS = ["NNG", "NNP", "NNBC", "NR", "NP", "VV", "VA", "SL", "SN", "VCP", "VCN"]

    # extract stems
    stems = [token[0] for token in me.pos(sentence) if token[1] in FILTERS]

    if stems:
        return ' '.join(stems).strip()
    else:
        return ''


def __job_add_stems(load_path, save_path):
    df = pd.read_excel(load_path)

    df['article_stem'] = df['title'] + '. ' + df['article']
    df['article_stem'] = df['article_stem'].map(lambda x: cleaning(x))
    df['article_stem'] = df['article_stem'].map(lambda x: nltk.sent_tokenize(x))
    df['article_stem'] = df['article_stem'].map(lambda x: [extract_only_stems(sentence) for sentence in x])
    df = df[['article_stem', 'date']]

    df.to_pickle(save_path)


def run(load_dir, save_dir, workers=8):
    # multi-processing
    p = Pool(processes=workers)

    for label in utils.listdir(load_dir):
        for company in tqdm(utils.listdir(load_dir, label), desc='extracting stems'):
            # make relevant directory
            os.makedirs(os.path.join(save_dir, label, company), exist_ok=True)

            # multi-processing
            files = utils.listdir(load_dir, label, company)
            load_paths = [os.path.join(load_dir, label, company, file_name) for file_name in files]
            save_paths = [os.path.join(save_dir, label, company, file_name.replace('.xlsx', '.pkl')) for file_name in files]
            p.starmap(__job_add_stems, zip(load_paths, save_paths))


def get_arguments():
    # Argument configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('--loaddir', type=str, default='data/crawled')
    parser.add_argument('--savedir', type=str, default='data/preprocessed')
    parser.add_argument('--workers', type=int, default=8)
    return parser.parse_args()


if __name__ == '__main__':
    # configurations
    args = get_arguments()
    load_dir = args.loaddir
    save_dir = args.savedir
    workers = args.workers

    # run
    run(load_dir, save_dir, workers)

