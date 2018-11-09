import time

import pandas as pd
import pymysql
import pickle

import requests

from utils.mysql import data_fetch


def merge_files():
    df = list()
    df.append(pd.read_excel("../../data/数据采集/财经1级账号共计（19）.xlsx"))
    df.append(pd.read_excel("../../data/数据采集/财经2级账号共计（103）.xlsx"))
    df.append(pd.read_excel("../../data/数据采集/财经3级账号共计（576）.xlsx"))
    df.append(pd.read_excel("../../data/数据采集/财经4级账号共计（2481）.xlsx"))
    df.append(pd.read_excel("../../data/数据采集/财经5级账号共计（16117）.xlsx"))
    df.append(pd.read_excel("../../data/数据采集/财经6级账号共计（13277）.xlsx"))

    df.append(pd.read_excel("../../data/数据采集/财经1级账号共计（1296）.xlsx"))

    with open("../../data/output/account_name.txt", 'w', encoding="utf8") as f:
        for d in df:
            for name in d["账号名"]:
                f.write(str(name) + "\n")


def name_fetch():
    conn = pymysql.connect(host="192.168.164.11", user="wechat", password="wechat", db='wechat', charset="utf8")
    with conn.cursor() as a:
        sql = "SELECT `name` FROM `wechat_public_accounts`;"
        a.execute(sql)
        data = a.fetchall()

    names = list()
    for item in data:
        names.append(item[0].replace(" ", "").replace('"', ""))

    dic = {}
    for name in names:
        if name in dic.keys():
            dic[name] += 1
        else:
            dic[name] = 1

    for item in dic:
        if dic[item] > 1:
            print("{}: {}".format(item, dic[item]))


# with open("../../data/temp/原始账户名列表.pickle", 'rb') as f:
#     data = pickle.load(f)
# 
# names = list()
# for item in data:
#     names.append(item[0].replace(" ", "").replace('"', ""))
# 
# names = list(set(names))

# with open("../../data/output/account_name_unique_hanlp.txt", 'w', encoding="utf8") as f:
#     for name in names:
#         f.write("{} nt 1\n".format(name))

# def merge_account():

# xl_file = pd.ExcelFile("../../../data/temp/0827+主题测试版 (1).xlsx")
# df = list()
# for sheetname in xl_file.sheet_names[1:]:
#     df.append(pd.read_excel("../../../data/temp/0827+主题测试版 (1).xlsx", sheet_name=sheetname))
# 
# with open("../../../data/output/account_name.txt", 'w', encoding="utf8") as f:
#     for d in df:
#         for name in d["公众号："]:
#             f.write(str(name) + "\n")


# with open("../../../data/output/medias.pickle", "rb") as f:
#     known_medias = pickle.load(f)
# 
# with open("../../../data/output/account_name.txt", "r") as f:
#     temp = f.readlines()
# l = []
# for item in temp:
#     if "、" in item:
#         l += item.split("、")
#     else:
#         l.append(item)
# temp = list(set(list(temp)))
# with open("../../../data/output/not_included.txt", 'w', encoding="utf8") as f:
#     for item in temp:
#         if item[:-1] in known_medias:
#             pass
#         else:
#             f.write(str(item))

with open("../../../data/output/not_included.txt", 'r', encoding="utf8") as f:
    data = f.readlines()

tic = time.time()
print(tic)
for item in data[49:59]:
    response = requests.post("http://10.0.0.22:4567/sogou/search/" + item[:-1])
    print(response.content.decode("utf8"))
toc = time.time()
print(toc - tic)

# 凤凰科技
# 郁言债市
# CITICS债券研究 
# 新浪科技
# 独角兽工厂
# pingwest品玩
# 极客视界
# 财鉴
# 阿尔法工厂
# 摩敦金融观察

# {"code":1,"msg":"SUCCESS","data":[{"nick":"广州凤凰科技","name":"gzfhkj"},{"nick":"无锡凤凰科技","name":"wuxifhkj"},{"nick":"凤凰科技他","name":"gh_ad357856b0cf"}]}
# {"code":211,"msg":"OBJECT_NOT_FOUND"}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"CITICS债券研究","name":"CiticsMacroBond"}]}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"新浪科技","found":true,"name":"techsina"}]}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"独角兽工厂","found":true,"name":"gh_a8e907028cb6"}]}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"PingWest品玩","name":"wepingwest"}]}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"极客视界","found":true,"name":"geekview"},{"nick":"VR极客视界","name":"gh_16c584552676"},{"nick":"雅极客视界","name":"hz-wxkj"}]}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"财鉴","found":true,"name":"CJ-caijian"},{"nick":"普世财鉴","name":"pru_finance"}]}
# {"code":1,"msg":"SUCCESS","data":[{"nick":"阿尔法工厂","found":true,"name":"Alpha_factory"}]}
# {"code":211,"msg":"OBJECT_NOT_FOUND"}

# output = data_fetch("*", "essays", "`media_nick`='独角兽工厂'")