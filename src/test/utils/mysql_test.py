from utils.mysql import *


def table_test():
    """
    
    :return: 
    """

    trial = 4

    if trial == 1:
        obj = CreateTable("author_media")

        obj.add_column("id", "VARCHAR", 32, "hashed ID", True)
        obj.add_column("name", "VARCHAR", 256, "作者用户名")
        obj.add_column("media_id", "VARCHAR", 32, "服务媒体ID")
        obj.add_column("media_nick", "VARCHAR", 256, "服务媒体名")
        obj.add_column("platform_id", "INT", 32, "来源平台ID")
        obj.add_column("essay_id", "VARCHAR", 32, "关系来源文章ID")
        obj.add_column("essay_pubdate", "DATETIME", "", "文章发布时间")
        obj.add_column("method", "VARCHAR", 32, "获取方式")
        obj.add_column("insert_time", "DATETIME", "", "插入时间")

        obj.create_table_sql()

        db = Database()
        obj.create_table(db.conn)

    if trial == 2:
        obj = CreateTable("media_media")

        obj.add_column("id", "VARCHAR", 32, "hashed ID", True)
        obj.add_column("media_id", "VARCHAR", 32, "服务媒体ID")
        obj.add_column("media_nick", "VARCHAR", 256, "服务媒体名")
        obj.add_column("platform_id", "INT", 32, "来源平台ID")
        obj.add_column("src_media_id", "VARCHAR", 32, "来源媒体ID")
        obj.add_column("src_media_nick", "VARCHAR", 256, "来源媒体名")
        obj.add_column("type", "VARCHAR", 32, "服务媒体ID")
        obj.add_column("essay_id", "VARCHAR", 32, "关系来源文章ID")
        obj.add_column("essay_pubdate", "DATETIME", "", "文章发布时间")
        obj.add_column("insert_time", "DATETIME", "", "插入时间")

        obj.create_table_sql()

        db = Database()
        obj.create_table(db.conn)

    if trial == 3:
        obj = CreateTable("user_behavior")

        obj.add_column("id", "INT", 11, "自增id", True, constraints="AUTO_INCREMENT")
        obj.add_column("uid", "VARCHAR", 32, "用户id", constraints="NOT NULL")
        obj.add_column("action", "VARCHAR", 128, "行为类型", constraints="NOT NULL")
        obj.add_column("pubdate", "DATETIME", "", "行为发生时间")
        obj.add_column("content", "text", "", "内容")
        obj.add_column("related_id", "VARCHAR", 32, "关联ID")
        obj.add_column("insert_time", "DATETIME", "", "插入时间")

        obj.create_table_sql()

        db = Database()
        obj.create_table(db.conn)
    
    if trial == 4:
        obj = CreateTable("essay_keywords")

        obj.add_column("essay_id", "VARCHAR", 32, "文章id", True, constraints="NOT NULL")
        obj.add_column("content", "text", "", "内容")
        obj.add_column("pubdate", "DATETIME", "", "发布时间时间")
        obj.add_column("insert_time", "DATETIME", "", "插入时间")

        obj.create_table_sql()

        db = Database()
        obj.create_table(db.conn)

    return obj


if __name__ == "__main__":
    _ = 1

    obj_test = table_test()
