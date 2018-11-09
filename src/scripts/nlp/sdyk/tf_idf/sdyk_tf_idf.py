import requests
from nlp.sdyk.tf_idf.sdyk_desc_data_fetch import fetch_all
from utils.text_cleaner import cleanup
import pickle


def sdyk_tfidf():
    data = fetch_all(62, "projects", "content, id", db="sdyk_raw_")
    url = "http://10.0.0.56:49002/tag?_q="

    dic = {}
    count = 0
    err_count = 0
    max_count = 0
    for item in data:

        if item[0] is None or len(item[0]) < 2:
            pass
        else:
            content = cleanup(item[0])
            id_num = item[1]
            sub_dic = {}
            item_list = content.replace("，", "。").replace(",", "。").replace(" ", "。").replace("、", "。").split("。")
            for tmp in item_list:
                if len(tmp) < 2:
                    pass
                elif len(tmp) > 199:
                    max_count += 1
                    print("Exceeded maximum length, count: {}".format(count))
                else:
                    try:
                        response = requests.get(url + tmp)
                        data = response.json()
                        lab = data['data']
                        for passage in lab['ps']:
                            for sentence in passage['ss']:
                                for word in sentence['ws']:
                                    if word['pos'] != "PU":
                                        w = word['c']
                                        if w in sub_dic:
                                            sub_dic[w] += 1
                                        else:
                                            sub_dic[w] = 1
                    except Exception as e:
                        err_count += 1
                        print(e)
                        print("Error count: {}".format(err_count))
            dic[id_num] = sub_dic
            count += 1
            if count % 20 == 0:
                print("Done row {}".format(count))
        # break

    with open("../../../data/output/doc_freq_.pickle", 'wb') as f:
        pickle.dump(dic, f)

