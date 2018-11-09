import pickle


def stopwords_update():
    """
    update stopwords list and store it into a binary file
    run after updating stopwords list
    :return: None
    """

    print("Updating stopwords: ...")
    stopwords = []
    with open("../../data/nlp/stop_words.txt", "r") as f:
        while 1:
            line = f.readline()
            if line == "":
                break
            stopwords.append(line[:-1])
    with open("../../data/temp/stop_words.pickle", "wb") as f:
        pickle.dump(stopwords, f)
    print("Updating stopwords: ... DONE")