import pymysql


def fetch_all(server, table, column="*", db="sdyk_raw", filters=""):
    """

    :param server:
    :param table:
    :param column:
    :param db:
    :param filters:
    :return:
    """
    if filters != "":
        filters = " " + filters

    if server == 61:
        conn61 = pymysql.connect(host="10.0.0.61", user="sdyk", password="sdyk", db=db, charset="utf8")
        with conn61.cursor() as a:
            sql = "SELECT {} FROM {}{};".format(column, table, filters)
            a.execute(sql)
        return a.fetchall()

    if server == 62:
        conn62 = pymysql.connect(host="10.0.0.62", user="root", password="sdyk", db=db, charset="utf8")
        with conn62.cursor() as a:
            sql = "SELECT {} FROM {}{};".format(column, table, filters)
            a.execute(sql)
        return a.fetchall()