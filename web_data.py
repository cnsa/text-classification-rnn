#!/usr/bin/env python
# coding=utf-8

import re, os, sys
import pandas as pd
import numpy as np

import nltk


def data_folder_path(data_folder=None):
    if data_folder is None:
        data_folder = 'cnsa'
    pathname = os.path.dirname(sys.argv[0])
    folder = os.path.join(pathname, 'data', data_folder) + '/'

    return folder


def clean_str(s):
    """Clean sentence"""
    s = re.sub(r"[^A-Za-zА-Яа-я0-9(),!?\'\`]", " ", s)
    s = re.sub(r"\'s", " \'s", s)
    s = re.sub(r"\'ve", " \'ve", s)
    s = re.sub(r"n\'t", " n\'t", s)
    s = re.sub(r"\'re", " \'re", s)
    s = re.sub(r"\'d", " \'d", s)
    s = re.sub(r"\'ll", " \'ll", s)
    s = re.sub(r",", " , ", s)
    s = re.sub(r"!", " ! ", s)
    s = re.sub(r"\(", " \( ", s)
    s = re.sub(r"\)", " \) ", s)
    s = re.sub(r"\?", " \? ", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r'\S*(x{2,}|X{2,})\S*', "xxx", s)
    s = re.sub(r'[^\x00-\x7F]+', "", s)
    return s.strip().lower()


def load_data_and_labels(filename):
    nltk.download('punkt')

    """Load sentences and labels"""
    df = pd.read_excel(filename)
    selected = ['Category', 'Text', 'Title']
    non_selected = list(set(df.columns) - set(selected))

    df = df.drop(non_selected, axis=1)  # Drop non selected columns
    df = df.dropna(axis=0, how='any', subset=selected)  # Drop null rows
    df = df.reindex(np.random.permutation(df.index))  # Shuffle the dataframe

    # Map the actual labels to one hot labels
    labels = sorted(list(set(df[selected[0]].tolist())))
    one_hot = np.zeros((len(labels), len(labels)), int)
    np.fill_diagonal(one_hot, 1)
    # mask = np.random.randint(0, 3, size=one_hot.shape).astype(np.bool)
    # one_hot[len(one_hot) - 1] = np.random.randint(0, 2)
    for idx, item in enumerate(one_hot):
        if one_hot[idx][len(item) - 1] < 1:
            one_hot[idx][len(item) - 1] = np.random.randint(0, 2)
    label_dict = dict(zip(labels, one_hot))

    # worker = lambda (xx): np.where(xx > 0)[0]
    #
    # for xs in np.nditer(x, op_flags=['readwrite']):
    #     x[...] = worker(xs)

    x_raw = df[selected[1]].apply(lambda x: clean_str(x)).tolist()
    y_raw = df[selected[0]].apply(lambda y: label_dict[y]).tolist()
    y_labels = multi_labels(y_raw, labels)
    return x_raw, y_labels, df, labels


def multi_labels(data, all_labels):
    new_data = []
    for labels in data:
        new_labels = []
        for i, flag in enumerate(labels):
            new_labels.append(all_labels[i]) if (flag > 0) else None
        new_data.append(new_labels)
    return new_data