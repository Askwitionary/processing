import pymysql
from nlp.wiki2mysql.wiki import Wikipedia
import pickle


conn = pymysql.connect(host="192.168.164.139", user="lduan", password="52192", db='wikipedia', charset="utf8mb4")


def drop_table():
    with conn.cursor() as c:
        sql = """DROP TABLE `wikipages`;"""
        c.execute(sql)
        conn.commit()


def create_table():
    with conn.cursor() as c:
        sql = """CREATE TABLE IF NOT EXISTS `wikipages` (`title` VARCHAR(256) NOT NULL, 
                                                         `id` VARCHAR(32) NOT NULL PRIMARY KEY, 
                                                         `ns` VARCHAR(16), 
                                                         `parent_id` VARCHAR(16),
                                                         `timestamp` VARCHAR(16) NOT NULL,
                                                         `model` VARCHAR(16),
                                                         `minor` VARCHAR(16),
                                                         `comment` LONGTEXT,
                                                         `contributor` LONGTEXT,
                                                         `format` VARCHAR(16),
                                                         `text` LONGTEXT
                                                         ) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;"""
        c.execute(sql)
        conn.commit()


def insert_data(w):
    with conn.cursor() as c:
        sql = """INSERT INTO `wikipages` (`title`, 
                                          `id`, 
                                          `ns`, 
                                          `parent_id`,
                                          `timestamp`,
                                          `model`,
                                          `minor`,
                                          `comment`,
                                          `contributor`,
                                          `format`,
                                          `text`
                                          ) 
                                          VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}'
                                   );""".format(w.title,
                                                w.id,
                                                w.ns,
                                                w.revision.parentID,
                                                w.revision.timestamp,
                                                w.revision.model,
                                                w.revision.minor,
                                                w.revision.comment,
                                                w.revision.contributor.username,
                                                w.revision.format_,
                                                w.revision.text)

        c.execute(sql)
        conn.commit()



def update_table():
    n = 0
    eee = 0
    success = 0
    errors = []
    with open("../../../data/wiki/zhwiki.xml", 'r', encoding="utf8") as f:
        n = 0
        temp_page = ""
        while True:
            line = f.readline()
            if line == "":
                break
            while line[0] == " ":
                line = line[1:]
            if line == "</page>\n":
                temp_page += line
                n += 1

                w = Wikipedia(temp_page)
                try:
                    insert_data(w)
                    success += 1
                    if success % 100 == 0:
                        print("Success count: {}".format(success))
                except Exception as e:
                    errors.append(w)
                    eee += 1
                    print(e)
                    print("Errors count: {}".format(eee))

                if n % 10000 == 0:
                    print("TOTAL count: {}".format(n))
            elif line == "<page>\n":
                temp_page = line
            else:
                temp_page += line
    with open("../../../data/temp/errors.pickle", 'wb') as f:
        pickle.dump(errors, f)


def just_some_test():
    n = 0
    eee = 0
    success = 0
    errors = []
    m = 0
    with open("../../../data/wiki/zhwiki.xml", 'r', encoding="utf8") as f:
        n = 0
        temp_page = ""
        while True:
            line = f.readline()
            if line == "":
                break
            while line[0] == " ":
                line = line[1:]
            if line == "</page>\n":
                temp_page += line
                n += 1

                w = Wikipedia(temp_page)
                try:
                    # insert_data(w)
                    if len(w.title) > 64:
                        print(w.title)
                        success += 1

                        if len(w.title) > m:
                            m = len(w.title)

                        print("==================== Count: {} Current Max: {} =====================".format(success, m))

                    # if success % 1000 == 0:
                    #     print("Success count: {}".format(success))
                except Exception as e:
                    errors.append(w)
                    eee += 1
                    print(e)
                    print("Errors count: {}".format(eee))

                if n % 10000 == 0:
                    print("TOTAL count: {}".format(n))
            elif line == "<page>\n":
                temp_page = line
            else:
                temp_page += line


if __name__ == "__main__":
    drop_table()
    create_table()
    update_table()