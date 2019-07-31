#-*- coding:utf-8 -*-
"""
author:TripleHack
date:20190428
train lr model
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV as LRCV


def train_lr_model(train_file, model_coef, model_file):
    """
    Args:
        train_file: process file for lr train
        model_coef: w1 w2
        model_file: model pkl
    """
    feature_count = 118
    feature_list = range(feature_count)
    train_label = np.genfromtxt(train_file, dtype = np.int32, delimiter = ",", usecols = -1)
    train_feature = np.genfromtxt(train_file, dtype = np.int32, delimiter = ",", usecols = feature_list)
    lr_cf = LRCV(Cs = [1, 10, 100], penalty = "l2", tol = 0.0001, max_iter = 500, cv = 5).fit(train_feature, train_label)
    scores = lr_cf.scores_.values()
    print(scores)
    # scores = lr_cf.scores_.values()[0]
    print("diff:%s" %(",".join([str(ele) for ele in scores.mean(axis = 0)])))
    print("Accuracy:%s" %(scores.mean()))
    lr_cf = LRCV(Cs = [1, 10, 100], penalty = "l2", tol = 0.0001, max_iter = 500, cv = 5, scoring = "roc_auc").fit(train_feature, train_label)
    scores = lr_cf.scores_.values()
    print("AUC:%s" %(scores))


if __name__ == "__main__":
    train_lr_model("../data/train_file", "", "")

