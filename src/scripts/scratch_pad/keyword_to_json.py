import pandas as pd

with open("../../../data/temp/keyword+总览.csv", "r") as f:
    data = f.readlines()

output = []
lvl2_kws = []

for line in data:
    ll = line.split(",")

    if ll[0] == "":
        if ll[1] == "":
            for word in ll[2:]:
                if word != "" and word != "\n":
                    lvl2_kws.append(word)
        else:
            if lvl2_kws != []:
                output.append({"pid": lvl1, "title": lvl2, "content": lvl2, "keywords": lvl2_kws})
            lvl2 = ll[1]
            print(lvl2_kws)
            lvl2_kws = []
            print("== ==" + lvl2)
            for word in ll[2:]:
                if word != "" and word != "\n":
                    lvl2_kws.append(word)

    else:
        lvl1 = ll[0]
        print("\n==" + lvl1)
        if ll[1] == "":
            pass
        else:
            lvl2 = ll[1]
            if lvl2_kws != []:
                output.append({"pid": lvl1, "title": lvl2, "content": lvl2, "keywords": lvl2_kws})
            print(lvl2_kws)
            lvl2_kws = []
            print("== ==" + lvl2)
            for word in ll[2:]:
                if word != "" and word != "\n":
                    lvl2_kws.append(word)
    
    # output.append({"pid": lvl1, "title": lvl2, "content": lvl2, "keywords": lvl2_kws})

if __name__ == "__main__":
    _ = 1
