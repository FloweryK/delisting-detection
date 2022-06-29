import os
import pandas as pd
import config
from tqdm import tqdm
from gensim.models.word2vec import Word2Vec


def make_w2v_model(load_dir=config.PROC_DIR, cache_model_dir=config.CACHE_MODEL_DIR,
                   min_count=5, size=300, workers=8, sg=1, window=5, iter=5):
    model_name = 'model_min=%02i_size=%04i_sg=%i_window=%i_iter=%i.w2v' % (min_count, size, sg, window, iter)
    model_path = os.path.join(cache_model_dir, model_name)

    if os.path.exists(model_path):
        print('w2v model found at:', model_path)
        model = Word2Vec.load(model_path)
    else:
        print("There is no cached model")
        sentences = get_sentences(load_dir)
        model = Word2Vec(sentences, min_count=min_count, size=size, workers=workers, sg=sg)
        print("Model is created")

        # cache the model
        os.makedirs(cache_model_dir, exist_ok=True)
        model.save(model_path)
        print("Model is saved as", model_name, "at", cache_model_dir)

    return model


def get_sentences(load_dir):
    sentences = []
    for label in os.listdir(load_dir):
        for company in tqdm(os.listdir(os.path.join(load_dir, label)), desc="gathering " + label + " companies"):
            for file in os.listdir(os.path.join(load_dir, label, company)):
                df = pd.read_pickle(os.path.join(load_dir, label, company, file))
                for article in df['article_stem'].to_list():
                    for sentence in article:
                        if sentence:
                            sentences.append(sentence.split())
    return sentences


if __name__ == '__main__':
    make_w2v_model(load_dir='data/preprocessed')