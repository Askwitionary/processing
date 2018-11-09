

with open("../../../../data/output/account_name_unique.txt", "r") as f:
    data = f.readlines()

with open("../../../../data/output/account_name_unique_jieba.txt", "w") as f:
    for item in data:
        f.write("{} {} {}\n".format(item[:-1], 1, "nt"))


if __name__ == "__main__":
    _ = 1