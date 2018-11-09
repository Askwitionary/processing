import pickle
from datetime import datetime

from pymysql import IntegrityError

from utils.mysql import data_fetch, Database
from utils.text_utilizer import get_md5

with open("../../../../data/szqj/medias.pickle", "rb") as f:
    known_medias = pickle.load(f)

data = data_fetch("`name`, `media_id`, `media_nick`, `platform_id`, `essay_id`, `essay_pubdate`", "author_media", host_IP="10.0.0.101", database="processing", limit=None)
connection = Database().conn
for item in data:
    platform_id = item[3]
    if platform_id == 1:
        platform = "WX"
        author_name = item[0]
        media_id = item[1]
        media_nick = item[2]
        essay_id = item[4]
        essay_pubdate = item[5]

        if author_name == media_nick:
            pass

        else:
            if author_name in known_medias:
                author_id = get_md5(platform + "-" + author_name)
                sql_cols = """`id`, `media_id`, `media_nick`, `platform_id`, `src_media_id`, `src_media_nick`, `type`, `essay_id`, `essay_pubdate`, `insert_time`"""
                sql_values = """VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                    get_md5("{}-{}-{}-{}".format(platform, media_id, author_id, essay_id)),
                    media_id,
                    media_nick,
                    platform_id,
                    author_id,
                    author_name,
                    "作者",
                    essay_id,
                    essay_pubdate,
                    datetime.now().replace(microsecond=0))
                sql = """INSERT INTO `media_media` ({}) {}""".format(sql_cols, sql_values)
                try:
                    with connection.cursor() as cur:
                        # print(sql)
                        cur.execute(sql)
                        connection.commit()
                except IntegrityError as e:
                    # print(e.args)
                    if e.args[0] == 1062:
                        pass
                    else:
                        print(e)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    _ = 1
