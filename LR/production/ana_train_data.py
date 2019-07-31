#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190425
feature selection and data selection
"""
import pandas as pd
import numpy as np
import operator
import sys

def get_input(train_data, test_data):
    """
    Args:
        input data
    Return:
        pd.DataFrame
    """
    dtype_dict = {"age":np.int32,
                  "education-num":np.int32,
                  "capital-gain":np.int32,
                  "capital-loss":np.int32,
                  "hours-per-week":np.int32}
    use_list = list(range(15))
    use_list.remove(2)
    train_df = pd.read_csv(train_data, sep = ",", header = 0, dtype = dtype_dict, na_values = " ?", usecols = use_list)
    train_df = train_df.dropna(axis = 0, how = "any")
    test_df = pd.read_csv(test_data, sep = ",", header = 0, dtype = dtype_dict, na_values = " ?", usecols = use_list)
    test_df = train_df.dropna(axis = 0, how = "any")
    return train_df, test_df

def label_trans(x):
    if x == " <=50K":
        return "0"
    if x == " >50K":
        return "1"
    return "0"


def process_label_feature(label_feature_str, df_in):
    """
    Args:
        label_feature_str:"label"
        df_in: DataFrameIn
    """
    df_in.loc[:,label_feature_str] = df_in.loc[:,label_feature_str].apply(label_trans)

def dict_trans(dict_in):
    """
    Args:
        dict_in: key str, value int
    Return:
        a dict: key str, value index
    """
    output_dict = {}
    index = 0
    for tuple in sorted(dict_in.items(), key = operator.itemgetter(1), reverse = True):
        output_dict[tuple[0]] = index
        index += 1
    return output_dict

def dis_to_feature(x, feature_dict):
    """
    Args:
        x: element
        feature_dict: pos dict
    Return:
        a str as "0,1,0"
    """
    output_list = [0] * len(feature_dict)
    if x not in feature_dict:
        return ",".join([str(ele) for ele in output_list])
    else:
        index = feature_dict[x]
        output_list[index] = 1
    return ",".join([str(ele) for ele in output_list])

def process_dis_feature(feature_str, df_train, df_test):
    """
    Args:
        feature_str
        df_train,df_test
    Return:
        the dim of the feature output
    process dis feature for lr train
    """
    origin_dict = df_train.loc[:,feature_str].value_counts().to_dict()
    feature_dict = dict_trans(origin_dict)
    df_train.loc[:, feature_str] = df_train.loc[:, feature_str].apply(dis_to_feature, args = (feature_dict, ))
    df_test.loc[:, feature_str] = df_test.loc[:, feature_str].apply(dis_to_feature, args = (feature_dict, ))
    # print(df_train.loc[:3, feature_str])
    return len(feature_dict)

def list_trans(input_dict):
    """
    Args:
        input_dict:{'count': 30162.0, 'mean': 38.437901995888865, 'std': 13.134664776856338, 'min': 17.0, '25%': 28.0, '50%': 37.0, '75%': 47.0, 'max': 90.0}
    Return:
        list: [0.1,0.2,0.3,0.4,0.5]
    """
    output_list = [0] * 5
    key_list = ["min","25%","50%","75%","max"]
    for index in range(len(key_list)):
        fixed_key = key_list[index]
        if fixed_key not in input_dict:
            print("error")
            sys.exit()
        else:
            output_list[index] = input_dict[fixed_key]
    return output_list

def con_to_feature(x, feature_list):
    """
    Args:
        x: element
        feature_list: list for feature trans
    Return:
        str: "1_0_0_0"
    """
    feature_len = len(feature_list) - 1
    result = [0] * feature_len
    for index in range(feature_len):
        if x >= feature_list[index] and x<= feature_list[index + 1]:
            result[index] = 1
            return ",".join([str(ele) for ele in result])
    return ",".join([str(ele) for ele in result])

def process_con_feature(feature_str, df_train, df_test):
    """
    Args:
        feature_str
        df_train,df_test
    Return:
        the dim of the feature output
    process con feature for lr train
    """
    origin_dict = df_train.loc[:, feature_str].describe().to_dict()
    feature_list = list_trans(origin_dict)
    df_train.loc[:, feature_str] = df_train.loc[:, feature_str].apply(con_to_feature, args = (feature_list, ))
    df_test.loc[:, feature_str] = df_test.loc[:, feature_str].apply(con_to_feature, args = (feature_list, ))
    return len(feature_list) - 1

def output_file(df_in, out_file):
    """
    write data of df_in to out_file
    """
    fw = open(out_file, "w+")
    for row_index in df_in.index:
        outline = ",".join([str(ele) for ele in df_in.loc[row_index].values])
        fw.write(outline + "\n")
    fw.close()



def ana_train_data(input_train_data, input_test_data, output_train, output_test):
    train_data, test_data = get_input(input_train_data, input_test_data)
    label_feature_str = "label"

    dis_feature_list = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country" ]
    con_feature_list = ["age","education-num","capital-gain","capital-loss","hours-per-week"]
    process_label_feature(label_feature_str, train_data)
    process_label_feature(label_feature_str, test_data)
    dis_feature_count = 0
    con_feature_count = 0
    for dis_feature in dis_feature_list:
        dis_feature_count += process_dis_feature(dis_feature, train_data, test_data)
    for con_feature in con_feature_list:
        con_feature_count += process_con_feature(con_feature, train_data, test_data)
    output_file(train_data, output_train)
    output_file(test_data, output_test)

    print(dis_feature_count)
    print(con_feature_count)

if __name__ == "__main__":
    ana_train_data("../data/train.txt", "../data/test.txt", "../data/train_file", "../data/test_file")
    # fp = open("../data/train_file")
    # count = 0
    # for line in fp:
    #     item = line.strip().split(",")
    #     print(len(item))
    #     count += 1
    #     if count >= 10:
    #         break
