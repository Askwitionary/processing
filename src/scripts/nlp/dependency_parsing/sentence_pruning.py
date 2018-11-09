from nlp.dependency_parsing.parser import Sentence
from utils.text_cleaner import html_cleanup


def pruning(txt):
    s = Sentence(txt)
    output = ""
    for w in s.parsed:
        if w.dependency in s.core_ind or w.id in s.core_ind:
            output += w.word
    return output


if __name__ == "__main__":
    # txt = "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
    # txt = "张先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"
    txt = "<p>这几天，有个新闻很重要，但被很多人忽略。就是北大资源和北大附中终于“在一起”了。<p>新闻是这样说的：近日，北大资源集团与北大附中战略合作签约仪式在京举行，双方宣布北大附中首批外埠学校将落地北大资源项目所在地――天津和开封。<p>邦主可以预见，看了这则新闻，很多人想拍邦主一板砖：这不就是学区房概念吗！只不过是北大附中！但也不值得邦主一惊一乍且专文论述吧！<p>且慢这么看！在这个最牛学区房的背后，邦主想表达的是，不要忘记这个“在一起”背后的一个关键信号：在万科郁亮所定义的“白银十年”，“服务”超越“关系”和资本，成为房地产市场一个新的核心竞争要素，而那些能击中客户需求的“痛点”，且能创造独特客户价值的房企，将有机会实现新一轮的“弯道超车”。<p><strong>1、“超车”的逻辑</strong><p>郁亮之所以把未来十年称为“白银十年”，意思是跟过去十年相比，虽然房产需求将大幅减少，但也有得做。而在这样的市场背景下，除了像融创这样定位于高端市场的公司继续满足改善性需求外，大量房企开始觊觎“社区运营”（其实年初孙宏斌也曾发微博说，融创今年要认真做好物业管理服务）。这样做有两方面的目的：一是开辟新的利润增长点，也就是从挣盖房子的钱，转变为挣为业主服务的钱；二是提升自身产品的附加价值，构筑差异化的市场竞争力。<p>最近在香港上市的“彩生活”，以及乐居和分众这几天正在力推的“实惠”，都属于前一种；而万科在社区内开食堂、运营养老公寓，北大资源在社区内开设新文化中心、北大医疗健康管理中心“双中心”，以及世茂房地产的“云服务”，则属于后一种。<p>在地产邦7月8日推送的“世茂副总裁蔡雪梅：高周转模式Out了，未来需要‘以利定产’”一文中，蔡雪梅认为，在房地产的“下半场”中，仅仅靠复制、靠提高周转率，这些招数都不足以胜出，“要能给客户全然不同的产品和服务，把服务作为整个开发商链条的重要一环，这个真的很有效。”<p>也就是说，未来服务做得好的房企，将有较高概率后来居上，成为市场的主流，而首要目标仍是冲规模的房企则要小心了。<p><strong>2、找准需求的“痛点”</strong><p>下半场是服务的竞争，其实现在已是共识了。不过，邦主在此提醒一声：不要为做服务而做，关键是要找准需求的“痛点”。比如说，万科开设“第五食堂”，确确实实解决了远郊小青年们的吃饭问题，而其养老公寓则解决的是，小青年们想把外地的父母接到一起生活，但可能又不太愿意住在同一个屋檐下的尴尬现实，况且，养老公寓还能提供必要的医疗服务。<p>邦主之所以拿“北大资源+北大附中”这个例子来重点分析，也主要是为了讲怎么找准市场需求的“痛点”。不少人知道五道口号称宇宙中心，就是因为五道口的房子是北京最好的学区房，每平方米高达10万元以上。<p>可以说，孩子的教育，是普天之下父母的一个“痛点”需求。北大资源集团董事长余丽告诉媒体，北大资源“追求”北大附中好多年，就是看中了这个“痛点”。<p>要知道，北大附中是名校中的名校，跟绝大多数学校把孩子当成考试机器不同的是，北大附中提倡的是一种“散养”式的教育理念，而这会让北大资源的客户“眼前一亮”，因为完全超出了预期嘛。<p>因此，做服务一定要找准“痛点”，不然就可能是隔靴搔痒。比如，海尔地产前几年就在做类似的事――开发业主之间沟通的“云平台”，但事实上一个社区的业主之间是很少沟通的，这件事后来也就不了了之了。<p><strong>3、服务要具备“稀缺性”</strong><p>物以稀为贵，稀缺的，才是最具价值且不可复制的。咱们中国人最喜欢一哄而上，你开“第五食堂”，我就开“第六食堂”，你有“云服务”，我就有“云云服务”，总之，你有我有全都有。<p>这种同质化的社区服务，不用猜今后肯定会大量涌现。这就要考验房企的运营管理能力了。如果管理得当，完全可以再出几个“彩生活”，但若管理不当，反而会拉低企业自身产品的竞争力。所以一定要慎之又慎。</p><p>不过，邦主认为最理想的状态是，你提供的“服务”，具有资源的稀缺性，有独特而不可复制的价值，五道口能成为宇宙中心，靠的就是学区房的“稀缺性”。<p>北大附中就具有这种“稀缺性”。北大附中此次落地天津和河南开封，是其建校以来首次直接投入师资和管理队伍在异地办校，可见其对扩张的慎重，但这也保证了这种学区房的稀缺性。<p>再比如北大资源今年暑期协办的北京大学“2014中学生考古文博训练营”，北大教授全程参与、讲解，北大资源项目所在的9个城市的中学生可报名参加，这种服务也具备“稀缺性”。<p>所以，我们可以得出，“白银十年”房企有两条路可走：一是社区运营管理制胜，可能管得好了，甚至都不收物业费了；二是独有资源制胜，试想，如果北大资源再带上北大医院，再次击中客户对于健康这一痛点需求，还有哪个开发商可以抵挡得住呢？<p>说到底，“白银十年”房企比拼的是整合优质、稀缺资源的能力。今后，会有更多的“北大资源+”、“万科+”、“世茂+”出现。至于“+”后面是什么，我们现在可能还难以想象。</p>"
    txt = html_cleanup(txt)
    sentences = txt.replace("！", "。").replace("？", "。").replace(".", "。").split("。")
    for sentence in sentences:
        print("Original: {} \n Pruned: {} \n".format(sentence, pruning(sentence)))
        print(Sentence(sentence))
        print("\n")


