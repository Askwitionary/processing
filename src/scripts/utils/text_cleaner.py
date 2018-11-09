import re


def html_cleanup(raw_html):
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, ' ', raw_html)
    return clean_text


def link_cleanup(raw_text):
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ', raw_text, flags=re.MULTILINE)
    return text


def filename_cleanup(raw_text):
    return re.sub(r'(下载|:)(.*?)(.jpeg|.jpg|.png|.doc)', " ", raw_text, flags=re.MULTILINE)


def punctuation_cleanup(raw_text):
    return re.sub(r'([.,/#!$%^&*;:{}=_`~()-])[.,/#!$%^&*;:{}=_`~()-]+', " ", raw_text)


def cleanup(raw_text: str):
    raw_text = raw_text.lower()
    return punctuation_cleanup(filename_cleanup(link_cleanup(html_cleanup(raw_text))))


if __name__ == "__main__":
    text = "HDMI============================================================50寸（显示区域680*1209mm)屏幕分辨率1920*1080PX屏幕比例16：9触摸屏10点红外触摸触摸分辨率4096*4096PX内置喇叭5W整机功率110W============================================================制作要求：基于触摸屏LED广告电视的界面"
    print(punctuation_cleanup(text))