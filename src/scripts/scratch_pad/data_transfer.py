import pymysql


class Article_raw:
    """

    """

    def __init__(self, row):
        self.wechat_id = row[0]
        self.wechat_name = row[1]
        self.biz = row[2]
        self.mid = row[3]
        self.title = row[4]
        self.pubdate = row[5]
        self.content = row[6]
        self.view_count = row[7]
        self.like_count = row[8]
        self.id = row[9]
        self.insert_time = row[10]
        self.update_time = row[11]

    def __repr__(self):
        return self.wechat_name


def data_transfer(total_limit=500, duplicate_limit=5):
    conn0 = pymysql.connect(host="192.168.164.139", user="lduan", password="52192", db='wechat_0', charset="utf8")
    conn1 = pymysql.connect(host="39.106.46.32", user="root", password="12345678", db='consulting', charset="utf8")
    with conn0.cursor() as a:
        sql = "SELECT * FROM `wechat_essays` LIMIT {};".format(total_limit)
        a.execute(sql)
        data = a.fetchall()

    final = []
    tmp = ''
    count = 0
    for item in data:
        article = Article_raw(item)
        if article.wechat_name == tmp:
            if count < duplicate_limit + 1:
                count += 1
                final.append(article)
            else:
                pass
        else:
            count = 0
            tmp = article.wechat_name


    import datetime
    with conn1.cursor() as a:
        for item in final:
            sql = """INSERT INTO `wechat_article` (`title`, `publish_date`, `create_time`, `content`, `full_content`, `from_type`, `author`, `wx_public_name`) 
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(item.title,
                                                                                    item.pubdate,
                                                                                    str(datetime.datetime.now()),
                                                                                    item.content[:100],
                                                                                    item.content,
                                                                                    2,
                                                                                    item.wechat_id,
                                                                                    item.wechat_name
                                                                                    )
            # print(sql)
            # break
            try:
                a.execute(sql)
                conn1.commit()
            except Exception as e:
                print(e)