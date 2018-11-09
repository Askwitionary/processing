import pandas as pd


df = pd.read_excel("../../data/temp/主题.xlsx")

file = pd.ExcelFile("../../data/temp/主题.xlsx")

dic = {}

for topic in file.sheet_names[1:]:

    selection = None
    df = pd.read_excel("../../data/temp/主题.xlsx", sheet_name=topic)
    for ind in df.keys():
        if "关键词" in ind:
            selection = ind
            break

    if selection is None:
        pass
    else:
        data = df[selection]
        keywords = []
        for word in data:
            if not pd.isna(word):
                word = str(word).replace("、", " ")
                if " " in word:
                    words = word.split(" ")
                    keywords += words

                else:
                    keywords.append(word)
        dic[topic] = keywords

df_out = pd.DataFrame.from_dict(dic, orient='index')
df_out = df_out.transpose()
writer = pd.ExcelWriter('../../data/output/关键词.xlsx')
df_out.to_excel(writer, '关键词')
writer.save()