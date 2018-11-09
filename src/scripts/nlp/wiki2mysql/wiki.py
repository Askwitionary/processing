import re
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps, loads
from mediawiki_parser.preprocessor import make_parser


def re_between_first(text, tag):
    r = re.search("<{}>(.*?)<\/{}>".format(tag, tag), text)
    if r is None:
        return None
    else:
        return r.group(1)


def re_between_first_m(text, tag):
    r = re.search("<{}>(.*?)<\/{}>".format(tag, tag), text, flags=re.S)
    if r is None:
        return None
    else:
        return r.group(1)


def re_between_findall(text, tag):
    r = re.findall("<{}>(.*?)<\/{}>".format(tag, tag), text, flags=re.S)
    if len(r) == 0:
        return None
    else:
        return r


class Contributor:
    def __init__(self, content):
        if content is None:
            content = ""
        self.username = re_between_first(content, "username")
        self.id = re_between_first(content, "id")


class Revision:
    def __init__(self, content):
        if content is None:
            content = ""
        self.id = re_between_first(content, "id")
        self.parentID = re_between_first(content, "parentid")
        self.timestamp = re_between_first(content, "id")
        self.contributor = Contributor(re_between_first_m(content, "contributor"))
        self.minor = re_between_first(content, "minor")
        self.comment = re_between_first(content, "comment")
        self.model = re_between_first(content, "model")
        self.format_ = re_between_first(content, "format")
        self.text = re.search("<text(.*?)<\/text>", content, flags=re.S)
        if self.text is not None:
            self.text = self.text.group(1)


class Wikipedia:
    def __init__(self, content):
        content = content.replace("'", '"')
        self.title = re_between_first(content, "title")
        self.ns = re_between_first(content, "ns")
        self.id = re_between_first(content, "id")
        self.revision = Revision(re_between_first_m(content, "revision"))


def chunky_read(filename, limit=10):
    with open("../../../data/wiki/{}.xml".format(filename), 'r', encoding="utf8") as f:
        n = 0
        pages = []
        temp_page = ""
        while n < limit:
            line = f.readline()
            if line == "":
                break
            while line[0] == " ":
                line = line[1:]
            if line == "</page>\n":
                temp_page += line
                n += 1
                pages.append(temp_page)
                # w = Wikipedia(temp_page)
            elif line == "<page>\n":
                temp_page = line
            else:
                temp_page += line
    return pages


# 3176788 pages
if __name__ == "__main__":
    fn = "zhwiki"
    data = chunky_read(fn)
    dics = []
    for item in data:
        json = dumps(bf.data(fromstring(item)))
        dic = loads(json)
        dics.append(dic)
    d = dics[2]
    text = d["page"]["revision"]["text"]["$"]
    templates = {}
    preprocessor = make_parser(templates)

    output = preprocessor.parse(text)