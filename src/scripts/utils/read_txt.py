
def read_txt(file_path):

    with open(file_path, "r", encoding="utf8") as file:
        data = file.readlines()

    return [data[i][:-1] for i in range(len(data))]


if __name__ == "__main__":
    print(read_txt("../../data/nlp/essay_author/author_keywords.txt"))
