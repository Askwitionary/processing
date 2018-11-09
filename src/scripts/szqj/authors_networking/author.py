from data_structure.graph.graph import Vertex, Edge, Graph
from utils.mysql import data_fetch


class Author(Vertex):

    def __init__(self, name, hobby):
        Vertex.__init__(self, name)
        self.hobby = hobby

dic = {}
data = data_fetch("wechat_name`, `meta_content", "wechat_essays_v1", limit=100000)
for item in data:
    wechat_name = item[0]
    content = item[1]
    entities = content.replace("：", " ").split(" ")

    for obj in entities:
        if "原创" in obj:
            entities.remove(obj)
        if "点击" in obj:
            entities.remove(obj)
    dic[wechat_name] = entities

# n = 0
# onehot = []
# for key in dic.keys():
#     n += len(dic[key])
#     onehot += dic[key]
#
# print("total: {} \n set: {}\n".format(n, len(set(onehot))))

n = 0
for key in dic.keys():
    for john in dic[key][:-1]:
        if john in dic.keys():
            n += 1
