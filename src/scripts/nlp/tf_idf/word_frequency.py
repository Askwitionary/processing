import pickle
import pandas as pd


def overall_frequency():
    """
    Input: word frequency dictionaries for each document as a list
    Input: desired keyword list

    Output: a .xlsx file that tells keyword frequency
    """

    with open("../../../data/output/word_freq.pickle", "rb") as f:
        frequency_list = pickle.load(f)

    overall = frequency_list[0]

    for dic in frequency_list[1:]:
        for key in dic.keys():
            if key in overall.keys():
                overall[key] += dic[key]
            else:
                overall[key] = dic[key]

    df = pd.read_excel("../../../data/output/关键词.xlsx")
    keywords = []

    for ind in df.keys():
        for word in df[ind]:
            if not pd.isna(word):
                keywords.append(str(word))

    keywords_freq = {}

    for kw in keywords:

        if kw in overall.keys():
            keywords_freq[kw] = overall[kw]
        else:
            keywords_freq[kw] = 0

    df_out = pd.DataFrame.from_dict(keywords_freq, orient='index')
    # df_out = df_out.transpose()
    writer = pd.ExcelWriter('../../../data/output/关键词词频.xlsx')
    df_out.to_excel(writer, '关键词词频')
    writer.save()


def document_frequency():
    """
    Input: word frequency dictionaries for each document as a list
    Input: desired keyword list

    Output: a .xlsx file that illustrates DOCUMENT FREQUENCY for the given keywords
    """

    with open("../../../data/output/word_freq.pickle", "rb") as f:
        frequency_list = pickle.load(f)

    df = pd.read_excel("../../../data/output/关键词.xlsx")
    keywords = []
    for ind in df.keys():
        for word in df[ind]:
            if not pd.isna(word):
                keywords.append(str(word))

    keywords_freq = {}

    for kw in keywords:
        for fre in frequency_list:
            if kw in fre.keys():
                if kw in keywords_freq.keys():
                    keywords_freq[kw] += 1
                else:
                    keywords_freq[kw] = 1
        if kw not in keywords_freq.keys():
            keywords_freq[kw] = 0
    df_out = pd.DataFrame.from_dict(keywords_freq, orient='index')
    # df_out = df_out.transpose()
    writer = pd.ExcelWriter('../../../data/output/关键词文频.xlsx')
    df_out.to_excel(writer, '关键词文频')
    writer.save()


overall_frequency()
document_frequency()
