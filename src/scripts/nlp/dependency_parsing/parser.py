from pyhanlp import HanLP
from utils.text_cleaner import html_cleanup


class Word:
    """
    Define object Word to store and process words
    """
    def __init__(self, raw: str):
        """
        Takes a string of the format given by HanLP
        :param raw:
        """

        self.raw = raw
        self.processed = self.process()

        # Building structure
        self.id = self.processed[0]
        self.word = self.processed[1]
        self.word2 = self.processed[2]
        self.pos1 = self.processed[3]
        self.pos2 = self.processed[4]
        self.nonsense1 = self.processed[5]
        self.dependency = self.processed[6]
        self.relationship = self.processed[7]
        self.nonsense2 = self.processed[8]
        self.nonsense1 = self.processed[9]

    def process(self):
        """

        :return:
        """

        processed = self.raw.split("\t")
        return processed

    def is_core(self):
        """

        :return:
        """

        return self.dependency == "0"


class Sentence:
    """
    Define Sentence object used to find dependencies using HanLP
    """
    def __init__(self, text):
        """
        Takes raw text data as input then parse and store processed data
        :param text: raw text input
        """

        # clean up html format non-sense
        self.text = html_cleanup(text)
        self.output_raw = str(HanLP.parseDependency(self.text))
        self.parsed, self.core_ind = self.parse()
        self.core_ind_update()

    def __str__(self):
        return self.output_raw

    def parse(self):
        """

        :return:
        """

        parsed = []
        lines = self.output_raw.split("\n")[:-1]
        core_ind = []
        for line in lines:
            obj = Word(line)
            if obj.is_core():
                core_ind.append(obj.id)
            parsed.append(obj)
        return parsed, core_ind

    def core_ind_update(self):
        while True:
            k = len(self.core_ind)
            for item in self.parsed:
                if item.dependency == self.core_ind[-1] and item.relationship == "并列关系":
                    self.core_ind.append(item.id)
            if len(self.core_ind) == k:
                break


if __name__ == "__main__":
    txt = "张先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"
    p = Sentence(txt)

