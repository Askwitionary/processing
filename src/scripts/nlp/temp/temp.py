import time
import pickle
import pyhanlp
import jieba
import pandas as pd
from utils.mysql import row_count, data_fetch
from utils.text_cleaner import html_cleanup
import multiprocessing as mp


# text = "我的天呐有限公司今  天发布了一个新闻: China’s infrastructure lesson for Africa"
# jieba.load_userdict("/home/lduan/PycharmProjects/processing/scripts/nlp/temp/temp.txt")
# seg = jieba.cut(text)
# for item in seg:
#     print(item)


def worker(w_id, start, end):
    with open("../../data/nlp/stop_words.pickle", "rb") as file:
        stopwords = pickle.load(file)

    df = pd.read_excel("../../data/output/关键词.xlsx")
    keywords = []

    for ind in df.keys():
        for word in df[ind]:
            if not pd.isna(word):
                keywords.append(str(word))

    with open("../../data/output/keywords.txt", "w", encoding="utf8") as file:
        for words in keywords:
            file.write("{} 3 nt\n".format(words))

    jieba.load_userdict("../../data/output/keywords.txt")

    n = start
    limit = 1000
    with open("../../data/output/train{}.dat".format(w_id), "w", encoding="utf-8") as f:
        while n < end:
            if end - n < limit:
                limit = end - n

            data = data_fetch("content",
                              "wechat_essays_v2",
                              limit=limit,
                              start=n,
                              host_IP="192.168.164.11",
                              database="wechat")
            for item in data:
                cleaned = html_cleanup(item[0])
                seg = jieba.cut(cleaned)
                output = ""
                for word in seg:
                    if word.replace(" ", "") == "":
                        pass
                    else:
                        if word not in stopwords:
                            output += word + " "
                f.write(output + "\n")
            n += limit
            print("id: {} === Done {} rows".format(id, n))


# num = row_count("wechat_essays_v2", host_IP="192.168.164.11", database="wechat")
# manager = mp.Manager()
# items = manager.list()
#
# process_num = 8
# inputs = []
# chunk = int(num / process_num)
# start = 0
# for i in range(process_num):
#     inputs.append((start, start + chunk))
#     start += chunk + 1
#
#
# counter = 0
# processes = []
# for input1, input2 in inputs:
#     processes.append(mp.Process(target=worker, args=(counter, input1, input2,)))
#     counter += 1
#
# # 运行所有进程
# for p in processes:
#     p.start()
#
# # 确定所有进程结束
# for p in processes:
#     p.join()

# with open("../../data/output/train0.dat", "r", encoding="utf-8") as f:
#     data = f.read()
# for i in range(1, 8):
#     with open("../../data/output/train{}.dat".format(i), "r", encoding="utf-8") as f:
#         data += f.read()
# with open("../../data/output/train.dat", "w", encoding="utf8") as f:
#     f.write(data)

# with open("../../data/output/train.dat", "r", encoding="utf8") as f:
#     data = f.readlines()

output = []
with open("../../data/temp/keyword+总览.csv", "r", encoding="utf8") as f:
    data = f.readlines()
for line in data:
    words = line.split(",")
    for w in words:
        if len(w) < 2:
            pass
        else:
            output.append(w)

with open("../../data/output/keyword+.csv", "w", encoding="utf8") as f:
    for item in output:
        f.write("{}, {}\n".format(item, ""))