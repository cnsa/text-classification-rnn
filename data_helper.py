#!/usr/bin/env python
# coding=utf-8

from multiprocessing import cpu_count

import numpy as np

from gensim.models.word2vec import Word2Vec

from nltk.downloader import download
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.stem import WordNetLemmatizer
import pymorphy2 as pm


def print_labels(pr):
    return " ".join(str(x) for x in pr)


def word_to_vec(newsline_documents, number_of_documents, document_Y, selected_categories, data_folder, model_name=None,
                num_features=500, document_max_num_words=100, load=False):
    download('wordnet')

    if model_name is None:
        model_name = 'reuters.word2vec'

    if load is True:
        # Load an existing Word2Vec model
        w2v_model = Word2Vec.load(data_folder + model_name)
    else:
        w2v_model = Word2Vec(newsline_documents, size=num_features, min_count=1, window=10, workers=cpu_count())
        w2v_model.init_sims(replace=True)
        w2v_model.save(data_folder + model_name)

    num_categories = len(selected_categories)
    X = np.zeros(shape=(number_of_documents, document_max_num_words, num_features)).astype(np.float32)
    Y = np.zeros(shape=(number_of_documents, num_categories)).astype(np.float32)

    empty_word = np.zeros(num_features).astype(np.float32)

    for idx, document in enumerate(newsline_documents):
        for jdx, word in enumerate(document):
            if jdx == document_max_num_words:
                break

            else:
                if word in w2v_model:
                    X[idx, jdx, :] = w2v_model[word]
                else:
                    X[idx, jdx, :] = empty_word

    for idx, key in enumerate(document_Y.keys()):
        Y[idx, :] = document_Y[key]

    return X, Y, num_categories


def tokenize_prepare():
    download('stopwords')


def tokenize_documents(document_X, document_Y, lang=None, regex=None):
    tokenize_prepare()

    if lang is None:
        lang = 'english'

    if regex is None:
        regex = '[\'a-zA-Z]+'

    # Load stop-words
    stop_words = set(stopwords.words(lang))

    # Initialize tokenizer
    # It's also possible to try with a stemmer or to mix a stemmer and a lemmatizer
    tokenizer = RegexpTokenizer(regex)

    # Initialize lemmatizer
    if lang is 'russian':
        analyzer = pm.MorphAnalyzer()
        lemmatizer = lambda (w): analyzer.parse(unicode(w))[0].normal_form
    else:
        analyzer = WordNetLemmatizer()
        lemmatizer = lambda (w): analyzer.lemmatize(w)

    # Tokenized document collection
    newsline_documents = []

    def tokenize(document):
        words = []

        for sentence in sent_tokenize(document):
            tokens = [lemmatizer(t.lower()) for t in tokenizer.tokenize(sentence) if
                      t.lower() not in stop_words]
            words += tokens

        return words

    # Tokenize
    for key in document_X.keys():
        newsline_documents.append(tokenize(document_X[key]))

    number_of_documents = len(document_X)

    return newsline_documents, number_of_documents


def print_predictions(predicted, x, classes, idx, y=None, with_keys=False, show_words=50):
    with_labels = []

    for item in predicted:
        pr = zip(classes, item)
        p = sorted(pr, key=lambda t: t[1], reverse=True)
        zipped = list(map((lambda x:
                           (x[0], float("%.3f" % x[1]))),
                          p[:5])
                      )
        with_labels.append(zipped)

    if with_keys is True:
        x_getter = lambda (i): x[i.astype(str)][:show_words].encode('utf-8') if i > 0 else None
    else:
        x_getter = lambda (i): x[i][:show_words].encode('utf-8') if i > 0 else None

    if y is None:
        y_getter = lambda (i): None
    else:
        y_getter = lambda (i): print_labels(y[i]).encode('utf-8')

    for i, pr in zip(idx, with_labels):
        line = x_getter(i)
        y_line = y_getter(i)
        labels_string = print_labels(pr).encode('utf-8')
        # cats = y_train_text[]

        print('{0} => {1} => {2}'.format(line, labels_string, y_line))


def update_frequencies(news_categories, categories, column='Newslines'):
    for category in categories:
        idx = news_categories[news_categories.Name == category].index[0]
        f = news_categories.get_value(idx, column)
        news_categories.set_value(idx, column, f + 1)

    return news_categories


def to_category_vector(categories, target_categories):
    vector = np.zeros(len(target_categories)).astype(np.float32)

    for i in range(len(target_categories)):
        if target_categories[i] in categories:
            vector[i] = 1.0

    return vector