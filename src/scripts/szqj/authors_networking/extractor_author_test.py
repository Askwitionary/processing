import pickle
import re

from utils.mysql import data_fetch
from utils.read_txt import read_txt
from utils.text_cleaner import html_cleanup


content = ""
essay_id = ""

start = 0
limit = 5000

data = data_fetch("`title`, `meta_content`, `content`", "essays", limit=limit, start=start)

with open("../../../data/temp/essays_tmp.pickle", "wb") as f:
    pickle.dump(data, f)

with open("../../../data/temp/essays_tmp.pickle", "rb") as f:
    data = pickle.load(f)

keywords = read_txt("../../../data/nlp/essay_author/author_keywords.txt")

black_list = ["图片来源", "配图来源", "来源为网络", "数据来源", "请勿转载", "转载以及向", "来源为网络"]

count = 0
for content in data:
    title = content[0]
    meta_data = content[1]
    if content[2] is not None:
        content = html_cleanup(content[2])
        # print(content)
        for kw in keywords:
            iter = re.finditer(kw, content)
            indices = [m.start(0) for m in iter]
            if len(indices) > 0:
                for ind in indices:
                    interesting = content[max(0, ind - 10):min(ind + 50, len(content))]
                    has_black_list = False
                    for blk in black_list:
                        if blk in interesting:
                            has_black_list = True
                            break
                    if not has_black_list:
                        # print(title)
                        print(interesting + "\n")
                        count += 1

print("Found {} matches".format(count))
