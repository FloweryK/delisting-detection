"""
By Minsang Yu, flowerk94@gmail.com
Edited by Hanbyeol Park, Minsang Yu
"""

import os
import torch
import random
import argparse
import numpy as np
import pandas as pd
import config
from tqdm import tqdm
from word2vec import make_w2v_model
from torch.utils.data import Dataset


class CompanyVectorData(Dataset):
    def __init__(self, load_dir=config.PROC_DIR, cache_model_dir=config.CACHE_MODEL_DIR, filters=config.FILTERS):
        # word2vec
        self.model = make_w2v_model(load_dir=load_dir, cache_model_dir=cache_model_dir,
                                    min_count=5, size=300, workers=8, sg=1, window=4, iter=5)
        self.dim = self.model.vector_size
        self.vocab = self.model.wv.vocab

        # prepare dataset
        self.data = self.make_data(load_dir=load_dir, filters=filters)

    def __getitem__(self, i):
        return {'x': torch.tensor(self.data[i][0], dtype=torch.float),
                'y': torch.tensor(self.data[i][1], dtype=torch.float)}

    def __len__(self):
        return len(self.data)


    def make_data(self, load_dir, filters):

        delisting_reason = self.load_delisting_reason()
        data = []

        for label in os.listdir(load_dir):
            for company in tqdm(os.listdir(os.path.join(load_dir, label)),
                                desc="making "+label+" company vector"):
                if (label == 'delisted') and self.is_filtered(delisting_reason[company], filters):
                    continue

                company_vector = []

                for file in os.listdir(os.path.join(load_dir, label, company)):
                    for article in pd.read_pickle(os.path.join(load_dir, label, company, file))['article_stem']:
                        article_vector = []

                        for sentence in article:
                            for word in sentence.split():
                                if word in self.vocab:
                                    article_vector.append(self.model.wv[word])

                        if article_vector:
                            company_vector.append(np.mean(article_vector, axis=0))

                if company_vector:
                    data.append((np.mean(company_vector, axis=0), [1] if label == 'delisted' else [0]))

        # balance labels and shuffle
        data = self.balance_labels(data)
        random.shuffle(data)

        return data

    def load_delisting_reason(self):
        df = pd.read_excel('src/delisted_list_2010.01.01-2020.06.25.xlsx')
        return {company: reason for company, reason in zip(df['회사명'], df['폐지사유'])}

    def is_filtered(self, reason, filters):
        for f in filters:
            if f in reason:
                return True
        return False

    def balance_labels(self, data):
        # split labels
        data_listed = [d for d in data if d[1][0] == 0]
        data_delisted = [d for d in data if d[1][0] == 1]
        min_num = min(len(data_listed), len(data_delisted))

        # sample
        data_listed = random.sample(data_listed, min_num)
        data_delisted = random.sample(data_delisted, min_num)
        data = data_listed + data_delisted

        return data



if __name__ == '__main__':
    dataset = CompanyVectorData(load_dir=config.PROC_DIR,
                                cache_model_dir=config.CACHE_MODEL_DIR,
                                filters=config.FILTERS)