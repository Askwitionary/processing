import re
import time

import requests
from requests_html import HTMLSession


class WebExtractor:
    timeout = 10  # 默认超时时间为5秒
    headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/7.2 (Windows 8 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    def __init__(self, url, keyword):
        self.url = url + keyword + '\"&tn=monline_dg&ie=utf-8'
        # self.html = self.get_html()

    def get_html(self):
        """
        爬取当前url所指页面的内容，保存到html中
        :return html字符串
        """
        r = requests.get(self.url, timeout=self.timeout, headers=self.headersParameters)
        if r.status_code == 200:
            html = r.text
        else:
            html = u''
            print('[ERROR]', self.url, 'get此url返回的http状态码不是200')
        return html

    def extract(self, selector):
        session = HTMLSession()
        r = session.get(self.url)
        return r.html.find(selector)


class SogouWeixin(WebExtractor):

    def __init__(self, keyword):
        self.url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query="
        WebExtractor.__init__(self, self.url, keyword)

    def extract_user_info(self):
        nick_selector = "#sogou_vr_11002301_box_0 > div > div.txt-box > p.tit > a > em"
        id_selector = "#sogou_vr_11002301_box_0 > div > div.txt-box > p.info > label"
        session = HTMLSession()
        r = session.get(self.url)
        try:
            nickname = r.html.find(nick_selector)[0].text
        except IndexError:
            nickname = None
        try:
            wechat_id = r.html.find(id_selector)[0].text
        except IndexError:
            wechat_id = None
        output = {"nickname": nickname, "wechat_id": wechat_id}
        return output


if __name__ == "__main__":
    _ = 1
    # while 1:
    #     obj = SogouWeixin("投行圈子")
    #     print(obj.extract_user_info())
    #     time.sleep(2)
    #     print(obj.get_html())
    url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=" + "投行圈子"
    session = HTMLSession()
    r = session.get(url)
