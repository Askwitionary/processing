import json
import pickle
import multiprocessing as mp
from datetime import datetime

import jieba

from nlp.tf_idf.tf_idf import tfidf
from utils.mysql import data_fetch, row_count, Database


def worker(w_id, start, end):
    print("===================Process {} has Started==============".format(w_id))

    with open("../../../../data/nlp/idf.pickle", "rb") as file:
        idf = pickle.load(file)
    connection = Database().conn
    n = start
    limit = min(end - start, 10000)
    
    dic_path = "../../../../data/output/account_name_unique_jieba.txt"
    jieba.load_userdict(dic_path)
    
    count = 1
    dup = 0
    print(end)
    while n < end:
        if end - n < limit:
            limit = end - n

        data = data_fetch(
            "`id`, `content`, `pubdate`",
            "essays",
            host_IP="192.168.164.15", user_name="raw", password="raw",
            database="raw", limit=limit, start=start, tail_condition="ORDER BY `insert_time`")

        for item in data:
            if item is None:
                pass
            else:
                essay_id = item[0]
                content = item[1]
                pubdate = item[2]

                if content is None:
                    pass
                else:
                    duplicated = 1
                    try:
                        duplicated = row_count("essay_keywords", condition="`essay_id` = '{}'".format(essay_id), host_IP="10.0.0.101", database="processing") > 0
                    except Exception as e:
                        print(e)
                    if duplicated:
                        dup += 1
                    else:
                        result = tfidf(content, idf, method=1)[0]
                        sql_cols = """`essay_id`, `content`, `pubdate`, `insert_time`"""
                        sql_values = """VALUES ('{}', '{}', '{}', '{}');""".format(
                            essay_id,
                            json.dumps(result, ensure_ascii=False),
                            pubdate,
                            datetime.now().replace(microsecond=0))
                        sql = """INSERT INTO `essay_keywords` ({}) {}""".format(sql_cols, sql_values)
                        try:
                            with connection.cursor() as cur:
                                # print(sql)
                                cur.execute(sql)
                                connection.commit()
                                count += 1
                        except Exception as e:
                            print(e)
            if (count + dup) % 1000 == 0:
                print("Process {} has inserted {} essays, duplicated skipped {} \n".format(w_id, count, dup))
        n += limit
        start += limit
    print("===================Process {} has ended==============".format(w_id))


num = row_count("essays", host_IP="192.168.164.15", database="raw")
# num = 666670
manager = mp.Manager()
items = manager.list()

process_num = 4
inputs = []
start_ind = 0
chunk = int((num - start_ind) / process_num)

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
