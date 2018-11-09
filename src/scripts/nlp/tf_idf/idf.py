import pickle
import os


content_whole = []
idf = {}
for filename in os.listdir("../../../../data/output/w_freq0/content/"):
    try:
        with open("../../../../data/output/w_freq0/content/" + filename, "rb") as f:
            content_whole = pickle.load(f)
            for essay in content_whole:
                for word in essay.keys():
                    if word in idf.keys():
                        idf[word] += 1
                    else:
                        idf[word] = 1
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

content_whole = []

with open("../../../../data/nlp/stop_words.pickle", "rb") as file:
    stopwords = pickle.load(file)

for word in stopwords:
    if word in idf.keys():
        pass
    else:
        idf[word] = 2**10

with open("../../../../data/nlp/idf.pickle", "wb") as file:
    pickle.dump(idf, file)

# with open("../../../../data/nlp/idf.pickle", "rb") as file:
#     idf = pickle.load(file)

if __name__ == "__main__":
    _ = 1