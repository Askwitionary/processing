import pandas as pd
import os

from utils.text_utilizer import cc2ec, replace_punctuation

# from openpyxl import load_workbook


path = "/home/lduan/PycharmProjects/processing/data/tengxiao/"
file_list = os.listdir(path)
scripts = pd.ExcelFile(path + file_list[0])
conversation = pd.ExcelFile(path + file_list[1])

# book = load_workbook("/home/lduan/PycharmProjects/processing/data/tengxiao/level+4+动画人物对白.xlsx")
# writer = pd.ExcelWriter("/home/lduan/PycharmProjects/processing/data/tengxiao/level+4+动画人物对白.xlsx", engine='xlsxwriter')
# writer.book = book
# writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

# def mark_it(worksheet, coor)

class Unit:

    def __init__(self):
        self.unit = None
        self.donghuasucai = None
        self.renwu = None
        self.content = None
        self.duibai = []


unit_dic = {}
a = 0
for sheet_name in scripts.sheet_names:
    sheet = scripts.parse(sheet_name, header=None).transpose()

    for i in range(sheet.shape[1]):
        if pd.isna(sheet[i][0]):
            pass
        else:
            obj = Unit()
            obj.unit = sheet[i][0].replace("\n", "")
            obj.donghuasucai = sheet[i][2]
            if pd.isna(sheet[i + 1][2]):
                sheet[i + 1][2] = ""
            obj.renwu = cc2ec(sheet[i + 1][2])
            obj.content = cc2ec(sheet[i + 2][1])
            unit_dic[a + 1] = obj
            a += 1


class Duibai:

    def __init__(self):
        self.index = None
        self.renwu = None
        self.content = None
        self.qita = None
        self.fanyi = None


a = 0
for sheet_name in conversation.sheet_names:
    sheet = conversation.parse(sheet_name, header=None).transpose()
    # sheet.to_excel(writer, sheet_name=sheet_name)
    for i in range(sheet.shape[1]):
        if pd.isna(sheet[i][0]):
            try:
                int(sheet[i][1])
                obj = Duibai()
                obj.index = int(sheet[i][1])
                if pd.isna(sheet[i][2]):
                    sheet[i][2] = ""
                obj.renwu = cc2ec(sheet[i][2])
                obj.content = cc2ec(sheet[i][3])
                obj.qita = sheet[i][4]
                obj.fanyi = sheet[i][5]
                # print(uuu)
                unit_dic[int(uuu)].duibai.append(obj)
            except ValueError:
                pass
        
        else:
            uuu = sheet[i][0].split(" ")[1]
        
for key in unit_dic.keys():
    unit = unit_dic[key]
    conv = unit.duibai
    for item in conv:
        if replace_punctuation(item.content).replace(" ", "").replace("\n", "").lower() in replace_punctuation(unit.content).replace(" ", "").replace("\n", "").lower():
            pass
        else:
            # print("{}: \n{} \n{}\n".format(unit.unit, item.content, unit.content))
            print("{}: \n{}: {} \n".format(unit.unit, item.renwu, item.content))
            _ = 1
    # break

for item in unit_dic[42].duibai:
    print(item.content)
# print(unit_dic[10].content)

# writer.save()

if __name__ == "__main__":
    _ = 1
