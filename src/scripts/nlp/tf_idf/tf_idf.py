import operator
import pickle
import time

import jieba
import pandas as pd
import requests

from utils.mysql import row_count, data_fetch
from utils.text_cleaner import html_cleanup
from utils.text_utilizer import text_spliter, isPureNumber, replace_punctuation


def get_word_freq():
    with open("../../../data/nlp/stop_words.pickle", "rb") as file:
        stopwords = pickle.load(file)

    df = pd.read_excel("../../../data/output/关键词.xlsx")
    keywords = []

    for ind in df.keys():
        for word in df[ind]:
            if not pd.isna(word):
                keywords.append(str(word))

    with open("../../../data/output/keywords.txt", "w", encoding="utf8") as file:
        for words in keywords:
            file.write("{} 3 nt\n".format(words))

    jieba.load_userdict("../../../data/output/keywords.txt")

    frequency = []
    num = row_count("wechat_essays", host_IP="192.168.164.11", database="wechat_v1")
    n = 0
    limit = 1000
    while n < num:
        if num - n < limit:
            limit = num - n

        data = data_fetch("content",
                          "wechat_essays",
                          limit=limit,
                          start=n,
                          host_IP="192.168.164.11",
                          database="wechat_v1")
        for item in data:
            fre = {}
            cleaned = html_cleanup(item[0])
            seg = jieba.cut(cleaned)
            for word in seg:
                if word.replace(" ", "") == "":
                    pass
                else:
                    if word not in stopwords:
                        if word in fre.keys():
                            fre[word] += 1
                        else:
                            fre[word] = 1
            frequency.append(fre)
        n += limit
        print("=== Done {} rows".format(n))

    with open("../../../data/output/word_freq.pickle", "wb") as file:
        pickle.dump(frequency, file)

    return frequency


def tfidf(content, idf, limit=50, method=0):
    with open("../../../../data/nlp/stop_words.pickle", "rb") as stopfile:
        stopwords = pickle.load(stopfile)
    
    # print("/".join(jieba.cut("众智财税智库告诉了我们一个严肃的道理")))
    content_dic = {}
    url = "http://10.0.0.59:49001/seg/s"
    # content = """<p>智联招聘日前发布的《2018年区块链人才供需与发展研究报告》显示，今年以来，区块链人才需求增长迅猛。以2017年第三季度的人才需求量为基数，2018年第二季度的区块链人才较2017年第三季度暴增636.83%。从分季度数据看，区块链人才的需求有逐步扩张的趋势，但波动也较大，随概念的热度呈现起伏态势。</p><p>区块链人才供应量充足但拥有技能的人十分稀少，过去一年向区块链相关岗位投递简历的人数远高于行业整体需求，是需求的3.6倍，从数量上看供给十分充足，人们对这个新兴领域的向往可见一斑。但具备区块链相关技能和工作经验的求职者，也就是存量人才仅占需求量的7%。</p><p><strong>区块链的人才需求主要集中在计算机、金融行业</strong></p><p>区块链职位最为集中的行业主要有互联网行业，占比35.2%居首；IT服务行业，占比20%；计算机软件行业，占比10.8%；以及基金证券行业，占比8.3%；网络游戏行业占比5.2%。需求结构与区块链技术落地的实际应用场景相关，业务发展速度较快的领域赢得了更多青睐。</p><p><strong>算法工程师和软件工程师是紧俏岗位</strong></p><p>算法工程师和软件工程师是紧俏岗位，但供给端基本空白：在企业需求方面，算法工程师是需求最多的岗位，占比10.9%，但投递量却很低。从存量人才结构上看，在核心技术岗位上的占比并不高，当前管理人员占比较高。</p><p><strong>区块链招聘需求集中在一线、新一线城市</strong></p><p>从目前区块链职位的城市分布来看，该领域的岗位需求主要集中在一线和新一线城市中。其中，北京、上海和深圳位于第一梯队，职位占比分别达到24%、20%和10%。杭州和广州紧随其后，分别占7%和5%。无一例外，北京、上海、广东、江苏、浙江和山东等省市，均颁布了区块链相关优惠政策和发展规划，鼓励区块链相关产业在当地创业和发展给予产业加持。</p><p><strong>区块链职位高薪难匹配存量人才薪酬更高</strong></p><p>需求的高速增长，加上满足条件的人才稀缺，企业想到的第一个手段就是通过高薪揽才。从薪酬分布区间来看，区块链招聘职位分布最多的区间为10000-15000元/月，占比23%；以及15000-25000元/月，占比29.2%。</p><p>智联招聘2018年第二季度全国37个主要城市的平均招聘薪酬为7832元/月，而区块链招聘职位中，8000元以上的高薪职位却占据了主流。可以看出，该领域的工资水平远远超过全国平均招聘薪酬，为了吸引供应有限的相关人才，企业不惜高薪抢人。</p><p>从投递供给人群看，他们当前薪酬主要集中在10001-15000元/月的区间，占比20.5%；6001-8000元/月区间占比19.1%，整体薪酬区间偏低，他们向往更高的薪酬。但从整体技能上来看，追求高薪确实存在挑战，这也导致虽然市场上有数倍于需求的人才供应量，但企业依然难招到合适的人才。</p><p>END</p><hr /><p><img src="https://mmbiz.qpic.cn/mmbiz_jpg/zq0bhlY6SQ5JvRRZKN4K9sNPBSicCqL0GNJ6kW8NiaFD3mXwPGc7QtiaGERNtGXqLxIO1KV4WYYRPeZbG2ibUTtfmQ/640?wx_fmt=jpeg"></p>"""
    content = replace_punctuation(html_cleanup(content))

    if content is None:
        c_result = None
    else:
        if method == 0:
            try:
                content = html_cleanup(content).replace(" ", "").replace("\n", "")

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
        elif method == 1:
            try:
                content = replace_punctuation(html_cleanup(content).replace(" ", "").replace("\n", ""))

                c_result = "/".join(jieba.cut(content))

            except KeyError:
                c_result = None
                pass

            except Exception as e:
                print(e)
                c_result = None
                time.sleep(1)
        else:
            c_result = None

    if c_result is None:
        return {}
    else:
        if method == 0:
            c_wordlist = c_result[1:-1].split(" ")
        elif method == 1:
            c_wordlist = c_result.split("/")
        else:
            c_wordlist = None
        for item in c_wordlist:
            if len(item) > 0 and item != " ":
                if item in content_dic.keys():
                    content_dic[item] += 1
                else:
                    content_dic[item] = 1

    for item in content_dic.keys():
        if isPureNumber(item):
            content_dic[item] = 0
        elif item in stopwords:
            content_dic[item] = 0
        else:
            try:
                item_idf = idf[item]
            except KeyError:
                item_idf = 1
            try:
                content_dic[item] = content_dic[item] / item_idf
            except ZeroDivisionError:
                content_dic[item] = 0

    ll = list(content_dic.items())
    ll.sort(key=operator.itemgetter(1), reverse=True)
    llout = ll[:min(limit, len(ll))]
    llfifty = ll[:min(50, len(ll))]
    output = {}
    fiftyshades = {}
    for item in llout:
        output[item[0]] = item[1]
    for item in llfifty:
        fiftyshades[item[0]] = item[1]
    return output, fiftyshades


if __name__ == "__main__":
    _ = 1

    with open("../../../../data/nlp/idf.pickle", "rb") as file:
        idf = pickle.load(file)
    content = """<p>智联招聘日前发布的《2018年区块链人才供需与发展研究报告》显示，今年以来，区块链人才需求增长迅猛。以2017年第三季度的人才需求量为基数，2018年第二季度的区块链人才较2017年第三季度暴增636.83%。从分季度数据看，区块链人才的需求有逐步扩张的趋势，但波动也较大，随概念的热度呈现起伏态势。</p><p>区块链人才供应量充足但拥有技能的人十分稀少，过去一年向区块链相关岗位投递简历的人数远高于行业整体需求，是需求的3.6倍，从数量上看供给十分充足，人们对这个新兴领域的向往可见一斑。但具备区块链相关技能和工作经验的求职者，也就是存量人才仅占需求量的7%。</p><p><strong>区块链的人才需求主要集中在计算机、金融行业</strong></p><p>区块链职位最为集中的行业主要有互联网行业，占比35.2%居首；IT服务行业，占比20%；计算机软件行业，占比10.8%；以及基金证券行业，占比8.3%；网络游戏行业占比5.2%。需求结构与区块链技术落地的实际应用场景相关，业务发展速度较快的领域赢得了更多青睐。</p><p><strong>算法工程师和软件工程师是紧俏岗位</strong></p><p>算法工程师和软件工程师是紧俏岗位，但供给端基本空白：在企业需求方面，算法工程师是需求最多的岗位，占比10.9%，但投递量却很低。从存量人才结构上看，在核心技术岗位上的占比并不高，当前管理人员占比较高。</p><p><strong>区块链招聘需求集中在一线、新一线城市</strong></p><p>从目前区块链职位的城市分布来看，该领域的岗位需求主要集中在一线和新一线城市中。其中，北京、上海和深圳位于第一梯队，职位占比分别达到24%、20%和10%。杭州和广州紧随其后，分别占7%和5%。无一例外，北京、上海、广东、江苏、浙江和山东等省市，均颁布了区块链相关优惠政策和发展规划，鼓励区块链相关产业在当地创业和发展给予产业加持。</p><p><strong>区块链职位高薪难匹配存量人才薪酬更高</strong></p><p>需求的高速增长，加上满足条件的人才稀缺，企业想到的第一个手段就是通过高薪揽才。从薪酬分布区间来看，区块链招聘职位分布最多的区间为10000-15000元/月，占比23%；以及15000-25000元/月，占比29.2%。</p><p>智联招聘2018年第二季度全国37个主要城市的平均招聘薪酬为7832元/月，而区块链招聘职位中，8000元以上的高薪职位却占据了主流。可以看出，该领域的工资水平远远超过全国平均招聘薪酬，为了吸引供应有限的相关人才，企业不惜高薪抢人。</p><p>从投递供给人群看，他们当前薪酬主要集中在10001-15000元/月的区间，占比20.5%；6001-8000元/月区间占比19.1%，整体薪酬区间偏低，他们向往更高的薪酬。但从整体技能上来看，追求高薪确实存在挑战，这也导致虽然市场上有数倍于需求的人才供应量，但企业依然难招到合适的人才。</p><p>END</p><hr /><p><img src="https://mmbiz.qpic.cn/mmbiz_jpg/zq0bhlY6SQ5JvRRZKN4K9sNPBSicCqL0GNJ6kW8NiaFD3mXwPGc7QtiaGERNtGXqLxIO1KV4WYYRPeZbG2ibUTtfmQ/640?wx_fmt=jpeg"></p>"""
    l = tfidf(content, idf)

    # get_word_freq()
    # with open("../../../data/output/word_freq.pickle", "rb") as f:
    #     freq_list = pickle.load(f)
