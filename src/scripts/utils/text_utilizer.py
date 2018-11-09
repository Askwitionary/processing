import hashlib
import re
import string


def cc2ec(text):
    return text.replace("，", ",").replace("。", ".").replace("？", "?").replace("！", "!").replace("：", ":").replace("；",
                                                                                                                  ";").replace(
        "”", '"').replace("“", '"').replace("’", "'")


def text_spliter(text, length=10000):
    output = []
    text = text + " "
    current_pos = 0

    betterbespace = text[length]

    while len(text) > length:
        spl = length
        while isPunctuation(betterbespace):
            spl += 1
            betterbespace = text[spl]

        output.append(text[current_pos:spl])
        text = text[spl:]

    output.append(text)
    return output


def isPureNumber(text):
    for char in text:
        if char not in "0.123456789-%年月日":
            return False
    return True


def isPunctuation(character, exception=""):
    pool = "，、。．？！～＄％＠＆＃＊‧；︰…‥﹐﹒˙·﹔﹕‘’“〝〞‵′〃|｜〔〕【】《》（）｛｝﹙﹚『』﹛﹜﹝﹞＜＞≦≧﹤﹥" \
           "「」︵︶︷︸︹︺︻︼︽︾〈〉︿﹀∩∪﹁﹂﹃﹄ /*-+.,?!@#$%^&*~`".replace(exception, "")

    return character in pool


def remove_punctuation(line, exception=""):
    if len(exception) == 0:
        rule = re.compile("[^a-zA-Z0-9\u4e00-\u9fa5]")
        line = rule.sub('', line)
    else:
        punctuation = """！？｡＂＃＄％＆＇（）＊＋－，。／：；＜＝＞＠［《》＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏""".replace(
            exception, "")
        punctuation += string.punctuation
        re_punctuation = "[{}]+".format(punctuation)
        line = re.sub(re_punctuation, "", line)

    return line.strip()


def replace_punctuation(line, replacement=" ", exception=""):
    punctuation = """！？｡＂＃＄％＆＇（）＊＋－，。／：；＜＝＞＠［《》＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏"""
    punctuation += string.punctuation
    for item in exception:
        punctuation = """！？｡＂＃＄％＆＇（）＊＋－，。／：；＜＝＞＠［《》＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏""".replace(item,
                                                                                                                 "")
    translator = str.maketrans(punctuation, replacement * len(punctuation))
    return line.translate(translator)


def get_md5(text):
    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    return m.hexdigest()


def re_between_findall(text, rule):
    r = re.findall(rule, text, flags=re.S)
    if len(r) == 0:
        return None
    else:
        return r


if __name__ == "__main__":
    _ = 1

    text = "微信公众号“中国金、融四,.,.,.,十人论坛”"
    print(remove_punctuation(text, exception="、"))
