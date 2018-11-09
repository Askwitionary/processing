import pickle
import multiprocessing as mp
import time

import requests

from utils.mysql import data_fetch, row_count
from utils.text_cleaner import html_cleanup
from utils.text_utilizer import replace_punctuation, isPunctuation


def text_spliter(text, length=5000):
    output = []
    text = text + " "
    current_pos = 0

    betterbespace = text[length]

    while len(text) > length:
        spl = length
        while isPunctuation(betterbespace):
            spl += 1
            betterbespace = text[spl]

        output.append(text[current_pos:spl])
        text = text[spl:]

    output.append(text)
    return output


def worker(w_id, start, end):
    print("===================Process {} has Started==============".format(w_id))
    if w_id % 2 == 0:
        url = "http://192.168.164.15:49001/seg/s"
    else:
        url = "http://10.0.0.59:49001/seg/s"
    with open("../../../../data/nlp/stop_words.pickle", "rb") as file:
        stopwords = pickle.load(file)

    n = start
    limit = min(end - start, 10000)

    title_whole = []
    content_whole = []
    count = 0
    tmp = 0

    while n < end:
        if end - n < limit:
            limit = end - n

        data = data_fetch(
            "`title`, `content`",
            "essays",
            host_IP="192.168.164.15", user_name="raw", password="raw",
            database="raw", limit=limit, start=start, tail_condition="ORDER BY `update_time`")

        for item in data:
            title_dic = {}
            content_dic = {}
            title = item[0]
            content = item[1]
            if title is None:
                t_result = None
            else:
                try:
                    title = html_cleanup(title).replace(" ", "").replace("\n", "")
                    t_result = requests.post(url, data={"_q": title}).json()["data"]
                except Exception as e:
                    print(e)
                    t_result = None
                    time.sleep(1)

            if content is None:
                c_result = None
            else:
                try:
                    content = html_cleanup(content).replace(" ", "").replace("\n", "")
                    # if len(content) > tmp:
                    #     tmp = len(content)
                    #     print(len(content))
                    #     print(content)

                    if len(content) < 10000:
                        c_result = requests.post(url, data={"_q": content}).json()["data"]
                    else:
                        content_list = text_spliter(content)

                        reqtoolong = [requests.post(url, data={"_q": item}).json()["data"] for item in content_list]

                        c_result = reqtoolong[0]
                        for evenmore in reqtoolong[1:]:
                            c_result = c_result + " " + evenmore

                except KeyError:
                    c_result = None
                    pass

                except Exception as e:
                    print(e)
                    c_result = None
                    time.sleep(1)

            if t_result is None:
                pass
            else:
                t_wordlist = t_result.split(" ")
                for item in t_wordlist:
                    if len(item) > 0:
                        # item_l = item.split("/")
                        # word = item_l[0]
                        # pos = item_l[1]
                        # if pos == "w":
                        #     pass
                        # else:
                        if item in stopwords:
                            pass
                        elif isPunctuation(item):
                            pass
                        else:
                            if item in title_dic.keys():
                                title_dic[item] += 1
                            else:
                                title_dic[item] = 1

            if c_result is None:
                pass
            else:
                c_wordlist = c_result[1:-1].split(" ")
                for item in c_wordlist:
                    if len(item) > 0:
                        # item_l = item.split("/")
                        # word = item_l[0]
                        # pos = item_l[1]
                        # if pos == "w":
                        #     pass
                        # else:
                        if item in stopwords:
                            pass
                        else:
                            if item in content_dic.keys():
                                content_dic[item] += 1
                            else:
                                content_dic[item] = 1

            title_whole.append(title_dic)
            content_whole.append(content_dic)

            count += 1
            if count % 1000 == 0:
                with open("../../../../data/output/w_freq/title/result{}.pickle".format(w_id), "wb") as f:
                    pickle.dump(title_whole, f)
                with open("../../../../data/output/w_freq/content/result{}.pickle".format(w_id), "wb") as f:
                    pickle.dump(content_whole, f)
                print("Process {} has processed {} essays... \n".format(w_id, count))
        n += limit
        start += limit
    with open("../../../../data/output/w_freq/title/result{}.pickle".format(w_id), "wb") as f:
        pickle.dump(title_whole, f)
    with open("../../../../data/output/w_freq/content/result{}.pickle".format(w_id), "wb") as f:
        pickle.dump(content_whole, f)

    print("===================Process {} has ended==============".format(w_id))


num = row_count("essays", host_IP="192.168.164.11", database="raw")
manager = mp.Manager()
items = manager.list()

process_num = 16
inputs = []
chunk = int(num / process_num)
start_ind = 0
for i in range(process_num):
    inputs.append((start_ind, start_ind + chunk))
    start_ind += chunk + 1

counter = 0
processes = []
for input1, input2 in inputs:
    processes.append(mp.Process(target=worker, args=(counter, input1, input2,)))
    counter += 1

# 运行所有进程
for p in processes:
    p.start()

# 确定所有进程结束
for p in processes:
    p.join()

# response = requests.post("http://10.0.0.59:49001/seg/s", data={"_q": data})

# with open("../../../../data/output/w_freq/content/result2.pickle", "rb") as f:
#     data = pickle.load(f)


# with open("../../data/output/train0.dat", "r", encoding="utf-8") as f:
#     data = f.read()
# for i in range(1, 8):
#     with open("../../data/output/train{}.dat".format(i), "r", encoding="utf-8") as f:
#         data += f.read()
# with open("../../data/output/train.dat", "w", encoding="utf8") as f:
#     f.write(data)
# 
# with open("../../data/output/train.dat", "r", encoding="utf8") as f:
#     data = f.readlines()


if __name__ == "__main__":
    _ = 1
