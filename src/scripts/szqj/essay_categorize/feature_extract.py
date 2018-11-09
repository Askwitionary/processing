import operator
import pickle

import jieba

from utils.text_utilizer import replace_punctuation

with open("../../../../data/output/file_tree.pickle", "rb") as f:
    file_tree = pickle.load(f)
with open("../../../../data/nlp/stop_words.pickle", "rb") as stopfile:
    stopwords = pickle.load(stopfile)
dic_path = "../../../../data/output/account_name_unique_jieba.txt"
jieba.load_userdict(dic_path)


w_f = {}

for lvl1 in file_tree:
    w_f[lvl1] = {}
    for lvl2 in file_tree[lvl1]:
        w_f[lvl1][lvl2] = []
        for file in file_tree[lvl1][lvl2]:
            tag = file[0]
            content = file[1]
            word_list = " ".join(w for w in jieba.cut(replace_punctuation(content, " ")))
            word_list = word_list.replace("\n", "").replace("  ", " ").split(" ")
            freq = {}
            
            for word in word_list:
                if word != "":
                    if word in freq.keys():
                        freq[word] += 1
                    else:
                        freq[word] = 1
            w_f[lvl1][lvl2].append(freq)

channel_freq = {}
for lvl1 in w_f.keys():
    channel_freq[lvl1] = {}
    for lvl2 in w_f[lvl1].keys():
        freq = {}
        for item in w_f[lvl1][lvl2]:
            for word in item.keys():
                if word in freq:
                    freq[word] += item[word]
                else:
                    freq[word] = item[word]
        channel_freq[lvl1][lvl2] = freq

idf = {}
for lvl1 in channel_freq.keys():
    for lvl2 in channel_freq[lvl1].keys():
        for word in channel_freq[lvl1][lvl2]:
            if word in idf.keys():
                idf[word] += 1
            else:
                idf[word] = 1
with open("../../../../data/nlp/idf_.pickle", "wb") as f:
    pickle.dump(idf, f)
tfidf = {}

for lvl1 in channel_freq.keys():
    tfidf[lvl1] = {}
    for lvl2 in channel_freq[lvl1].keys():
        tfidf[lvl1][lvl2] = []
        for word in channel_freq[lvl1][lvl2]:
            tfidf[lvl1][lvl2].append((word, channel_freq[lvl1][lvl2][word] / idf[word]))

output = []
for lvl1 in tfidf.keys():
    for lvl2 in  tfidf[lvl1].keys():
        ll = tfidf[lvl1][lvl2]
        ll.sort(key=operator.itemgetter(1), reverse=True)
        llout = ll[:15]
        llout = [item[0] for item in llout]
        output += llout



with open("../../../../data/nlp/essay_onehot__.pickle", "wb") as f:
    pickle.dump(list(set(output)), f)

if __name__ == "__main__":
    _ = 1