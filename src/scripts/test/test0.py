import operator
import pickle
import time
from datetime import datetime

import requests
import hashlib
import pymysql
import re

from utils.mysql import data_fetch, Database
from utils.text_cleaner import html_cleanup
from utils.text_utilizer import replace_punctuation, get_md5, isPureNumber

# conn = pymysql.connect(host="192.168.164.139", user="lduan", password="52192", db='wikipedia', charset="utf8")
# with conn.cursor() as a:
#     sql = "SELECT `comment` FROM wikipages where `id` = '102577';"
#     a.execute(sql)
#     data = a.fetchall()


#
# import pickle
# import numpy as np
#
# with open("../../data/temp/tmp.pickle", 'rb') as f:
#     data = pickle.load(f)
#
# dd = [int(data[i][0]) for i in range(len(data))]
# nn = np.array(dd)
#
# import pyhanlp

# from nlp.wiki2mysql.wiki import Wikipedia, re_between_first
# f = open("../../data/wiki/zhwiki.xml", 'r', encoding="utf8")
# pages = []
# temp_page = ""
# while True:
#     line = f.readline()
#     while line[0] == " ":
#         line = line[1:]
#     if line == "</page>\n":
#         temp_page += line
#         pages.append(temp_page)
#     elif line == "<page>\n":
#         temp_page = line
#     else:
#         temp_page += line
#
#     if len(pages) > 999:
#         break
# print(pages[2])
# # w = Wikipedia(pages[2])
#
# rr = re.findall("<id>(.*)</id>", pages[2])
# r = re_between_first(pages[2], "id")
# for page in pages:
#     w = Wikipedia(page)
#     if len(w.ns) > 1:
#         print(w.title)
#         print(w.ns)


# conn = pymysql.connect(host="192.168.164.11", user="wechat", password="wechat", db='wechat', charset="utf8")
# with conn.cursor() as a:
#     sql = "SELECT `content` FROM wechat_essays;"
#     a.execute(sql)
#     data = a.fetchall()
#
# for d in data:
#     if "原创" in d[0]:
#         print(d[0])


# m = hashlib.md5()
# m.update("WX-明佣宝".encode("utf-8"))
# print(m.hexdigest() == "001d3b0485a9e67771e85f6d9b469d33")


# text = """<p><strong>马云突如其来的出手，让日本措手不及！</strong></p><p><strong>一</strong></p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Ybpib5Sr9SmIibaBOlZ2EkwibpcmUt6qJAypugnZnOOI3PcK8m84rrbL6EhHiaH1chDtIwu6CX3IvRC944wpq4YI4w/640?wx_fmt=png"></p><p><strong>日本公交</strong></p><p><strong>日本</strong>传来大消息，继全面进入中国城市公交系统后，支付宝正联手欧力士，一举杀入日本城市公交系统！</strong></p><p><strong>谁是欧力士？</strong>日本最大综合金融服务集团，资产规模近900亿美元，向日本超40万家企业提供金融服务。</p><p><strong>双方决定：</strong>从今天开始首先在日本旅游胜地冲绳试验。手机“滴”一声完成所有购票流程，快速进站乘车。</p><p><strong>这将是中国的移动支付首次进入日本交通系统！意味着，日本人出门搭公交地铁，也将被支付宝承包！</strong></p><p><strong>二</strong></p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Ybpib5Sr9SmIibaBOlZ2EkwibpcmUt6qJAyPpkud6XvO4b6QTqV7TSKGZgd8jA5Hu26LNIaldVlv6PbLwH773F0WA/640?wx_fmt=png"></p><p><strong>日本今日报纸</strong></p><p><strong>消息一出，日本炸了！</strong></p><p><strong>“马云要来了”、“我们的公交车要被占领了”.</strong>....,日本媒体甚至不惜动用头版头条大喊：中国巨人打来了！</p><p><strong>毫无疑问</strong>，日本媒体慌了，但日本消费者却激动不已。他们欢呼：终于可以像中国人一样刷手机坐车了。</p><p><strong>日本铁路</strong>则更加兴奋，冲绳的一家单轨铁路公司，昨日就按耐不住正式宣布，全面接入中国的支付宝。</p><p><strong>据透露，这次将把日本原本只能读取纸质车票的自动检票机全面大改，实现可一秒读取支付宝的二维码！</strong></p><p><strong>三</strong></p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Ybpib5Sr9SmIibaBOlZ2EkwibpcmUt6qJAyrVagbtDvZiagIlcHMQhpWcwgmG2JkaXqD7ONYeB6TrQADqAMicJlZib7A/640?wx_fmt=png"></p><p><strong>马云到底要做什么？三个字：全球付！</strong></p><p><strong>今天，你只看到日本的交通系统</strong>，却不知日本全国的肯德基、3万家店铺商场、50000辆出租车已全部接入支付宝。</p><p><strong>今天，你只看到日本的惊呼</strong>，却不知支付宝已覆盖全球超200个国家和地区，服务着这个地球上超8亿的人口。</p><p><strong>这给我们最明显的改变就是，去一个国家，不用再兑换这个国家的货币。而是拿着支付宝，用人民币结算！</strong></p><p><strong>四</strong></p><p><strong><img src="https://mmbiz.qpic.cn/mmbiz_jpg/SHrrySx9fb4cV7urOz3DkXt2nhBlkGgOU7nicGcwwKvFiajKFngSJX8xal7Jiaq96020AuEicMy8bQ5SZZ0tYxoAwQ/640?"></strong></p><p><strong>没错，他的战场已是全世界！</strong></p><p><strong>早在2017年，欧洲国家摩纳哥宣布：举国接入支付宝，打造全球首个无现金国家！</strong></p><p>这是历史上第一个派出国家首脑，由最高政府与支付宝签约的国家。也是马云第一次与主权国家政府签订协议。</p><p>据了解，这个国家有三分之一人口都是百万美元以上的富豪，人均GDP高达163036美元，是世界上民众最富有的国家。</p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Ybpib5Sr9SmIhUNRSOuGRUXlMzHFZ2QMG6BurJ9DfSmEj8cRszoXutZATl9JeIyNxemjRX3cyiaOSQ9dymUzxblg/640?wx_fmt=png"></p><p><strong>马云的支付宝欧洲版图（蓝色区域）</strong></p><p><strong>从那一刻起，马云正式拿下包含英国、法国、意大利在内的12大欧洲国家。把中国的移动支付、普惠理念带到了全世界！</strong></p><p>同是2017年，马云联手支付集团First Data Corp，让支付宝造福美国人民！</p><p>目前，First Data服务的商户高达400万，而苹果的移动支付服务覆盖量是450万。</p><p><strong>这意味着，在美国，支付宝的实力足以同苹果的Apple Pay分庭抗礼！</strong></p><p>今天，当世界将目光投向马云和支付宝的时候，他们更看重的，是腾飞中的中国经济样本和经济力量。</p><p><strong>再困难，也磨不灭马云进军世界的决心！</strong></p><p><strong>再压迫，也挡不住中华民族企业的崛起！</strong></p><p><strong>五</strong></p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Ybpib5Sr9SmL0A0lLceQQjFTYPibia00QPYZAe4ibAkCGpPBMpmF7gnXbmIibKAibAubfkHAibTOrLEpl2fn6dBGUdlLA/640?wx_fmt=png"></p><p><strong>你以为这就结束了？马云全球付的终极目标是全球通用！</strong></p><p><strong>何为“全球通用”？</strong>即为日本人拿着“日本版支付宝”，在中国也能支付结算，甚至是任何一个支持支付宝的国家。</p><p>现在支付宝已经出现：<strong>马来西亚版（touch）、韩国版（kakao pay）、菲律宾版（Mynt）、印尼版（DANA）、印度版（paytm）、孟加拉版（bKash）、泰国版（Ascend Money）</strong>，日本版正在推进。</p><p><strong>未来将会怎样？全世界各个国家的人民拿着自己的手机，装着“当地版支付宝”，走遍世界、刷遍世界！</strong></p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Ybpib5Sr9SmIibaBOlZ2EkwibpcmUt6qJAyl5zH4O3E7gQwibtDGia5ibq79sxjichWn2XpISt4icoicklosnroNd7QeEPw/640?wx_fmt=png"></p><p><strong>没错，马云正构建一个全球支付体系，让全世界的货币都可以在支付宝上高效的流通，无国界、无种族、无宗教！</strong></p><p>很多人都在惊叹支付宝<strong>每天十亿、百亿</strong>的货币流通，但背后的本质却是千千万万陌生人正因此建立信任。</p><p><strong>货币流通驱动信用流通</strong>，这样的模式一旦从中国复制到全世界，支付宝将成为全球人民的“移动世界银行”！</p><p><strong>所以，放大你的格局吧！少看点国内你争我夺的窝里斗，看看中国企业正在如何改变世界！</strong></p><h2>史上首次!刚刚，又一触目惊心数据公布，日本最大危机上演</h2><p>日本正在遭遇史上最严峻的人口危机!</p><p>继日本新生人口数创历史新低后，9月16日，<strong>日本总务省又公布了一个“噩耗”。</strong></p><p><strong>日本70岁以上的老龄人口比例史上首次超过20%，</strong>达到20.7%，即2618万。 一年前，该比例为19.9%。</p><p>而日本65岁以上的老年人也达到了创纪录的3557万人，比上年同期增加了44万人，占总人口数的28.1%，同样创下历史新高。</p><p>更可怕的是，据日本国立社会保障和人口问题研究所预计，到2040年日本老龄人口的比例将达到35.3%。</p><p>无疑，人口问题成了日本最头疼的麻烦，安培晋三甚至直接称其为“国难”。</p><p>然而，<strong>任凭政府怎么呼吁，日本人却依旧我行我素</strong>，晚婚或不婚，生一个或者不生！</p><p><strong>(一)</strong></p><p>经济评论家大前研一曾在《低欲望社会：胸无大志的时代》一书中这样写道：请加微信公众号：工业智能化(robotinfo) 马云都在关注</p><p>“<strong>年轻人没有欲望、没有梦想、没有干劲，日本已陷入低欲望社会!</strong>”</p><p><strong>这是一种什么生活状态？</strong></p><p>简单的说，面对着越来越高的生活成本，导致日本年轻人越来越丧气。</p><p>于是，很多人不买车不买房，穿着平价快时尚的衣服，吃着超市的便当、饭团。</p><p>而除了工作外，在其它的时间中则更愿意独自宅在家里，将大量的时间花费在手机、电脑上，<strong>完全不想和异性去培养感情。</strong></p><p>在他们看来，结婚生子是一笔非常大的开销，连自己都养不起，更别提养活全家了。</p><p><strong>与其让自己背上一身的债，还不如就那么一直单身着!</strong></p><p>根据日本家族计划协会近年发表的报告，在年龄介于16至49岁的1134名受访者中，<strong>49.3%在过去一个月中没有性生活。</strong></p><p><strong>随之而来的则是结婚、新生儿数量的减少。</strong></p><p>相关数据显示，<strong>2017新婚情侣数为60.7万对</strong>，比2016年减少1.4万对，这也是二战之后结婚人数最少的一年。</p><p>2017年，<strong>日本新生人口数只有94.6万，创历史新低</strong>，而死亡人数却达到134.4万人，这意味着2017年，日本人口自然减少40.3万人!</p><p>更甚的是，对未来经济发展趋势的不安，正让<strong>日本年轻人越来越佛系</strong>。</p><p>很多人已经习惯了这样的“低欲望”生活方式，且没有欲望通过努力去打破它。</p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/hryAAmuez2gNVKRulowN117g3usaB0UT6WRepDc1tIrksGW8lspG9NkXbBVeCr1JzFBX3K5Q4jj43TwSDFX2Yw/640?wx_fmt=png"></p><p>对于一个国家来说，只要少子化的情况一直存在，社会的老龄化就会越来越严重。</p><p>日本年轻人的生活状态，无疑预示着，<strong>日本的人口失衡问题必将愈演愈烈！</strong></p><p><strong>(二)</strong></p><p><strong>这对日本实在不是什么好事情！</strong></p><p>人口危机除了潜移默化中打击着年轻人对未来的积极心态外。</p><p>“交养老年金的人越来越少，领养老年金的人越来越多”的情况，更是让<strong>社保体系陷入了崩溃的边缘。</strong></p><p>众所周知，早在在上世纪60年代，日本就建立起了全民社保。</p><p>彼时，其覆盖范围之广、福利待遇之高在世界上都是数一数二的。</p><p>这在经济繁荣期倒也没什么。</p><p>然而，三十年后，随着日本经济陷入 “失去的二十年”，麻烦随之来了。</p><p>根据2018年度国家财政预算执行计划显示，全年度国家预算总额为95万亿日元(约5万7000亿元人民币)，但是<strong>用于养老和医保等的社保领域的支出，已经占到了国家预算总额的三分之一</strong>，达到了32万亿日元。</p><p>这就意味着，2018年，<strong>国家三分之一的钱，将被用于国民的养老和治病等民生领域!</strong></p><p><strong>而为了自救，如履薄冰的日本政府已开始在老年人身上做起文章。</strong></p><p>就在不久前，日本首相安倍晋三在接受《日本经济新闻》采访时表示，将讨论把继续雇用的年龄提高至65岁以上，以打造不论到多大年纪、只要有意愿就能参加工作的<strong>“终身不退休”、“终身活跃”</strong>的社会。</p><p>事实上，即使政府不倡导“终身不退休”，<strong>日本的老年人也早已迫于生活的压力不得不继续出来工作。</strong></p><p>在日本，开出租车的司机多数是白发苍苍的男性老年人。</p><p>此外，工地看护、交通保安、物业管理员、清洁员、邮政速递员、超市收银员等职业中也都活跃着老年人的身影。</p><p>不仅如此，还有一群老人，因担心养不活自己，便剑走偏锋，<strong>用故意犯罪的方式寻求入狱。</strong></p><p>日本官方2015《犯罪白皮书》数据显示，与20年前相比，该年度的老人犯罪人数翻了<strong>4.6倍</strong>。</p><p>岁月无情，是人就总有干不动的一天，</p><p>但现实是如此的悲哀，经济的不景气让“颐养天年”在日本成了奢侈。</p><p>这正是日本眼下正在发生的危机！</p><p>年轻人越来越萎靡，老年人却被逼着去奋斗，更可怕的是政府对此还无计可施......</p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Y1bPSq8tOvH0Zm2UP1468tUX2aXUVRq3Fow7D0LzyWw82FLerIFRibogcP398E3c65MMPyMqMvaD6zgK3G667icg/640?wx_fmt=png"></p><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Y1bPSq8tOvEZuYWP3cLjUibNCxAS5SVA8GT40WSVz7zXPN8GCvD3k4v6CUDyvhmAxAHsr6rqLYnBBQicFknh8Cag/640?wx_fmt=png"></p><h3>【关于版权：本平台致力于寻找互联网行业至关重要的文章，以提高全民互联网意识，推动共享经济学习和项目落地，促进行业交流，共同学习进步。精选的每一篇文章，都会注明作者和来源(除非实在找不到)，文章版权归作者所有。如涉及文章版权问题，请及时联系我们删除。欢迎投稿。联系信箱：845769534@qq.com】</h3><p><img src="https://mmbiz.qpic.cn/mmbiz_png/Y1bPSq8tOvEZuYWP3cLjUibNCxAS5SVA8JRXDwiaFfWd5Iiab6eLg86FK0nSMRJfJQ28A9aJV8cSJLvBXY8gnVcmQ/640?wx_fmt=png"></p>"""
# 
# text = replace_punctuation(html_cleanup(text).replace(" ", ""))
# result = requests.post("http://localhost:8080/seg/nshort/", data={"text": text})
# 
# print(result.text)




# with open("../../../data/output/medias.pickle", "rb") as f:
#     known_medias = pickle.load(f)
# 
# data = data_fetch("`name`, `media_id`, `media_nick`, `platform_id`, `essay_id`, `essay_pubdate`", "author_media",
#                   host_IP="10.0.0.101", database="processing", limit=None)
# connection = Database().conn
# big_dic = {}
# 
# for item in data:
#     platform_id = item[3]
#     if platform_id == 1:
#         platform = "WX"
#         author_name = item[0]
#         media_id = item[1]
#         media_nick = item[2]
#         essay_id = item[4]
#         essay_pubdate = item[5]
# 
#         if author_name == media_nick:
#             pass
# 
#         else:
#             if author_name in big_dic.keys():
#                 big_dic[author_name].append({"platform_id": platform_id,
#                                              "platform": platform,
#                                              "media_id": media_id,
#                                              "media_nick": media_nick,
#                                              "essay_id": essay_id,
#                                              "essay_pubdate": essay_pubdate})
#             else:
#                 big_dic[author_name] = [{"platform_id": platform_id,
#                                              "platform": platform,
#                                              "media_id": media_id,
#                                              "media_nick": media_nick,
#                                              "essay_id": essay_id,
#                                              "essay_pubdate": essay_pubdate}]
# 
# with open("../../../data/output/author_media_dic.pickle", "wb") as f:
#     pickle.dump(big_dic, f)

with open("../../../data/output/author_media_dic.pickle", "rb") as f:
    big_dic = pickle.load(f)

count_dic = {}

for item in big_dic.keys():
    if len(item) > 1 and not isPureNumber(item):
        if len(big_dic[item]) > 8:
            print("{}: {}".format(item, len(big_dic[item])))
    
#     if len(big_dic[item]) in count_dic:
#         count_dic[len(big_dic[item])] += 1
#     else:
#         count_dic[len(big_dic[item])] = 1
# ll = list(count_dic.items())
# 
# ll.sort(key = operator.itemgetter(0))

# print(ll)
# print(max_len)