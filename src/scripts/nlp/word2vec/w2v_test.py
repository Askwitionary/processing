import pickle
import string
import random
import numpy as np
import bisect
import time
import multiprocessing as mp
import os
import threading


# os.system("taskset -p 0xff %d" % os.getpid())



# class Test:
#     def __init__(self):
#         self.name = 'test'
#         self.id = random.random()
#
# dic = Test()
# with open('test.pickle', 'wb') as f:
#     pickle.dump(dic, f, protocol=pickle.HIGHEST_PROTOCOL)
#
# k = open('test.pickle', 'rb')
# d = pickle.load(k)

# dic = {}
# with open('../data/word2vec_c', 'r') as f:
#     while True:
#         line = f.readline()
#         if line == '':
#             break
#         ll = line[:-1].split(' ')
#         dic[ll[0]] = np.array(ll[1:]).astype(np.float)
#
# with open('../data/w2v.pickle', 'wb') as f:
#     pickle.dump(dic, f)





class My_thread (mp.Process):

    def __init__(self, word):
        mp.Process.__init__(self)
        self.word = word

    def run(self):
        print("Starting {}".format(self.word))
        output(self.word)
        print("Exiting {} \n \n".format(self.word))


def similar_words(word, length):
    tic2 = time.clock()
    with open('../../../data/word2vec/w2v.pickle', 'rb') as f:
        dic = pickle.load(f)
    toc2 = time.clock()
    tot2 = toc2 - tic2
    word = word
    vec = dic[word]



    tot1 = 0
    # tot2 = 0
    minimum = []

    for key in dic.keys():

        value = dic[key]

        if np.shape(value) == np.shape(vec):
            # print(np.dot(dic[key], vec))
            tic = time.clock()
            diff = np.linalg.norm(dic[key] - vec)
            # diff = np.dot(dic[key], vec)
            toc = time.clock()
            tot1 += toc - tic
            if len(minimum) < length:
                minimum.append((diff, key))
                minimum.sort()

            else:
                bisect.insort(minimum, (diff, key))

                minimum = minimum[:-1]

    # print("Step1 time for {}: {}".format(word, tot1))
    # print("Step2 time for {}: {} \n \n".format(word, tot2))
    return minimum


def output(word):
    ttic = time.clock()
    print("Starting word: {} \n".format(word))
    words = similar_words(word, 10)
    print("Input word: {} \n".format(word))
    for item in words:
        print("Word: {}    Diff: {}".format(item[1], item[0]))
    ttoc = time.clock()
    print("Total time for {}: {} \n \n ".format(word, ttoc - ttic))
    return 0



# def output1():
#     for i in range(100000000000):
#         j = i**2
#     return 1
#
#
# def output2():
#     for i in range(100000000000):
#         j = i + 2
#     return 2


if __name__ == '__main__':

    # out = mp.Queue()
    # q = mp.Queue()
    # p1 = mp.Process(target=output1())
    # p2 = mp.Process(target=output2())
    # words = ["大佬", "美女", "童年", "学习", "异常", "刺激", "色情", "抽烟", "完美", ]
    words = ["财经", "金融", "股票", "证券", "异常", "刺激", "色情", "抽烟", "完美", ]
    process_list = []
    for w in words[:6]:
        process_list.append(mp.Process(target=output, args=(w,)))

    for p in process_list:
        p.start()
    for p in process_list:
        p.join()

    print("Exiting main thread \n")
    # print(q.get())


