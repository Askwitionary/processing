from datetime import datetime

from utils.mysql import data_fetch, Database


class Behaviour:

    def __init__(self, action, data):
        if action == "channel":
            self.uid = data[1]
            self.action = action
            self.time_occurred = data[5]
            channel_details = \
                data_fetch("`title`, `content`, `pid`, `id`, `show`", "biz_channels", "id={}".format(data[0]),
                           host_IP="192.168.164.11", user_name="dwapi", password="api@szqj",
                           database="dw_biz")[0]
            self.description = str({"id": data[2],
                                    "data": {
                                        "title": channel_details[0],
                                        "content": channel_details[1],
                                        "pid": channel_details[2],
                                        "id": channel_details[3],
                                        "show": channel_details[4]}}).replace("'", '"')
            self.related_id = data[0]

        if action == "search":
            self.uid = data[0]
            self.action = action
            self.time_occurred = data[7]
            self.description = str(
                {"content": data[1], "count": data[3], "type": data[4], "status": data[2], "id": data[5]}).replace("'",
                                                                                                                   '"')
            self.related_id = data[1][:min(len(data[1]), 32)]

        if action == "topic":
            self.uid = data[1]
            self.action = action
            self.time_occurred = data[5]
            topic_details = data_fetch(
                "`title`, `content`, `id`, `sources`, `filters`, `fav_count`, `status`, `only_match_title`, `uid`",
                "biz_topics", "id={}".format(data[0]),
                host_IP="192.168.164.11", user_name="dwapi", password="api@szqj",
                database="dw_biz")[0]
            # print(topic_details)
            self.description = str({"id": data[3],
                                    "enable": str(data[2]),
                                    "data": {"title": topic_details[0],
                                             "content": topic_details[1],
                                             "id": topic_details[2],
                                             "sources": topic_details[2],
                                             "filters": topic_details[2],
                                             "fav_count": topic_details[2],
                                             "status": topic_details[2],
                                             "only_match_title": topic_details[2],
                                             "uid": topic_details[2],
                                             }}).replace("'", '"')
            self.related_id = data[0]

        if action == "eclick":
            self.uid = data[0]
            self.action = action
            self.time_occurred = data[2]
            self.description = str({"outbound_time": data[3], "view_percent": data[4], "id": data[5]}).replace("'", '"')
            self.related_id = data[1]

        if action == "elike":
            self.uid = data[1]
            self.action = action
            self.time_occurred = data[4]
            self.description = str({"id": data[2]}).replace("'", '"')
            self.related_id = data[0]

        if action == "ecomment":
            self.uid = data[1]
            self.action = action
            self.time_occurred = data[9]
            self.description = str({"content": data[2],
                                    "to_uid": data[3],
                                    "f_id": data[4],
                                    "f_comment": data[5],
                                    "like_count": data[6],
                                    "status": data[7],
                                    "id": data[8]}).replace("'", '"')
            self.related_id = data[0]

        if action == "efav":
            self.uid = data[1]
            self.action = action
            self.time_occurred = data[5]
            self.description = str({"enable": data[2], "id": data[3]}).replace("'", '"')
            self.related_id = data[0]

    def gen_sql(self):

        sql_cols = """`uid`, `action`, `pubdate`, `content`, `related_id`, `insert_time`"""
        sql_values = """VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""".format(
            self.uid,
            self.action,
            self.time_occurred,
            self.description,
            self.related_id,
            datetime.now().replace(microsecond=0))
        return """INSERT INTO `user_behavior` ({}) {}""".format(sql_cols, sql_values)

    def insert_data(self, connection):
        sql = self.gen_sql()
        try:
            with connection.cursor() as cur:

                cur.execute(sql)
                connection.commit()
        except Exception as e:
            print(sql)
            print(e)


host_IP = "192.168.164.11"
db_name = "dw_biz"
uname = "dwapi"
pword = "api@szqj"

channel_data = data_fetch("`channel_id`, `uid`,`id`, `insert_time`, `update_time`", "biz_user_channels", limit=None,
                          host_IP=host_IP, user_name=uname, password=pword,
                          database=db_name)
search_data = data_fetch("`uid`, `content`, `status`, `result_count`, `type`, `id`, `insert_time`, `update_time`",
                         "biz_search_records", limit=None, host_IP=host_IP, user_name=uname, password=pword,
                         database=db_name)
topic_data = data_fetch("`topic_id`, `uid`, `enable`, `id`, `insert_time`, `update_time`", "biz_topic_subscribers",
                        limit=None, host_IP=host_IP, user_name=uname, password=pword,
                        database=db_name)
click_data = data_fetch("`uid`, `essay_id`, `visit_time`, `outbound_time`, `view_percent`, `id`,"
                        " `insert_time`, `update_time`",
                        "biz_user_essay_visits", limit=None, host_IP=host_IP, user_name=uname, password=pword,
                        database=db_name)
essay_like_data = data_fetch("`essay_id`, `uid`, `id`, `insert_time`, `update_time`", "biz_essay_favs", limit=None,
                             host_IP=host_IP, user_name=uname,
                             password=pword, database=db_name)
comment_data = data_fetch("`essay_id`, `uid`, `content`, `to_uid`, `f_id`, `f_comment`, "
                          "`like_count`, `status`, `id`, `insert_time`, `update_time`",
                          "biz_essay_comments", limit=None, host_IP=host_IP, user_name=uname, password=pword,
                          database=db_name)
fav_data = data_fetch("`essay_id`, `uid`, `enable`, `id`, `insert_time`, `update_time`", "biz_essay_favs", limit=None,
                      host_IP=host_IP, user_name=uname, password=pword,
                      database=db_name)

db = Database()

for item in channel_data:
    Behaviour("channel", item).insert_data(db.conn)

for item in search_data:
    Behaviour("search", item).insert_data(db.conn)

for item in topic_data:
    Behaviour("topic", item).insert_data(db.conn)

for item in click_data:
    Behaviour("eclick", item).insert_data(db.conn)

for item in essay_like_data:
    Behaviour("elike", item).insert_data(db.conn)

for item in comment_data:
    Behaviour("ecomment", item).insert_data(db.conn)

for item in fav_data:
    Behaviour("efav", item).insert_data(db.conn)

if __name__ == "__main__":
    _ = 1
