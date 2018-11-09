import re
import pymysql
import pickle
import numpy
import matplotlib

from utils.text_cleaner import html_cleanup
from utils.read_txt import read_txt
from utils.mysql import data_fetch
from utils.web_utilizer import SogouWeixin
from utils.text_utilizer import isPunctuation, re_between_findall, remove_punctuation

# data = data_fetch("title`, `meta_content", "wechat_essays_v2", limit=1000)
#
# for item in data:
#     title = item[0]
#     meta_data = item[1]
#     authors = meta_data.split(" ")
#     if len(authors) > 1:
#         pass
#     else:
#         pass

#
# with open("../../data/temp/essays_tmp.pickle", "wb") as f:
#     pickle.dump(data, f)


# start = 0
# limit = 50000

# data = data_fetch("`title`, `meta_content`, `content`", "essays", limit=limit, start=start)

with open("../../../data/temp/essays_tmp.pickle", "rb") as f:
    data = pickle.load(f)


def info_extract(content):
    account_associate_rules = read_txt("../../../data/nlp/essay_author/account_associate_rules.txt")
    author_associate_rules = read_txt("../../../data/nlp/essay_author/author_associate_rules.txt")
    author_blklist = read_txt("../../../data/nlp/essay_author/author_blklist.txt")
    account_blklist = read_txt("../../../data/nlp/essay_author/account_blklist.txt")
    count = 0
    media_list = []
    author_list = []
    if content is not None:
        content = html_cleanup(content)
        for auth_rule in author_associate_rules:
            result = re_between_findall(content, auth_rule)
            if result is not None:
                for item in result:
                    s = remove_punctuation(item[1], exception="、")
                    if s != "":
                        authors = s.split("、")
                        for auth in authors:
                            if len(auth) < 2:
                                break
                            else:
                                blk = 0
                                for blk_item in author_blklist:
                                    if blk_item in auth:
                                        blk += 1
                                if blk:
                                    pass
                                else:
                                    count += 1
                                    author_list.append(auth)

        for acc_rule in account_associate_rules:
            result = re_between_findall(content, acc_rule)
            if result is not None:
                for item in result:
                    s = remove_punctuation(item[1], exception="、")
                    if s != "" and len(s) == len(item[1]):
                        medias = s.split("、")
                        for media in medias:
                            if len(media) < 2:
                                break
                            else:
                                # obj = SogouWeixin(media)
                                # info = obj.extract_user_info()
                                # print("What we found: {} \nWhat we got: {}".format(media, info["nickname"]))
                                # if media == info["nickname"]:
                                if len(media) > 22 and "、" not in media:
                                    pass
                                else:
                                    blk = 0
                                    for blk_item in account_blklist:
                                        if blk_item in media:
                                            blk += 1
                                    if blk:
                                        pass
                                    else:
                                        count += 1
                                        media_list.append(media)
                                    # print(media.replace(" ", "").replace("文丨", ""))
    return [list(set(media_list)), list(set(author_list))]


# data = data_fetch("`nick`", "media", limit=21000)
# data = [data[i][0] for i in range(len(data))]
# with open("../../../data/output/medias.pickle", "rb") as f:
#     data = pickle.load(f)
# 
# maxlen = 0
# for item in data:
#     if len(item) > maxlen:
#         maxlen = len(item)
#         print(item)
# print(maxlen)


# contain = 0
# for media in media_list:
#     if media in data:
#         contain += 1

if __name__ == "__main__":
    _ = 1
    for item in data:
        if item[2] is not None:
            result = info_extract(item[2])
            if result != [[], []]:
                print(info_extract(item[2]))
