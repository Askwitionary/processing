import pickle


def redesign():
    with open("../../../data/output/doc_freq_.pickle", 'rb') as f:
        dic = pickle.load(f)

    words_dic = {}

    for item in dic:
        for word in dic[item]:
            if word in words_dic:
                words_dic[word].append(item)
            else:
                words_dic[word] = [item]

    for item in words_dic:
        words_dic[item] = len(list(set(words_dic[item])))

    # with open("../../../data/output/df.pickle", 'wb') as f:
    #     pickle.dump(words_dic, f)
    return words_dic


from utils.text_cleaner import cleanup
import requests


class TextRank:
    def __init__(self, text):
        self.raw = text
        self.cleaned = cleanup(text)
        self.df = self.get_df()
        self.word_count = 0
        self.score = self.rating()

    @staticmethod
    def get_df():
        with open("../../../data/output/df.pickle", 'rb') as f:
            dic = pickle.load(f)
        return dic

    def rating(self):
        url = "http://10.0.0.56:49002/tag?_q="
        score = 0

        if self.cleaned is None or len(self.cleaned) < 2:
            pass
        else:
            content = self.cleaned
            item_list = content.replace("，", "。").replace(",", "。").replace(" ", "。").replace("、", "。").split("。")
            for tmp in item_list:
                if len(tmp) < 2:
                    pass
                elif len(tmp) > 199:
                    print("Exceeded maximum length")
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
                                        self.word_count += 1
                                        if w in self.df:
                                            score += 1 / self.df[w]
                                        else:
                                            score += 1/1
                    except Exception as e:
                        print(e)
        return score / self.word_count


import time
import operator
from nlp.sdyk.tf_idf.sdyk_desc_data_fetch import fetch_all


if __name__ == "__main__":

    tmp_list = []
    data = fetch_all(62, "projects", "content", filters="WHERE category='宣传片制作'")
    for content in data:
        content = content[0]
        tic = time.clock()
        a = TextRank(content)
        tmp_list.append((a.cleaned, a.score, time.clock() - tic))
    tmp_list.sort(key=operator.itemgetter(1), reverse=True)
    for t in tmp_list:
        print("{} \n Got score: {:3f} in {:3f} secs \n".format(t[0], t[1], t[2]))
