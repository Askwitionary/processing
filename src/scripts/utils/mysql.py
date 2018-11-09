import pymysql


class Database:

    def __init__(self, host_IP="10.0.0.101", username="lduan", pword="52192", database="processing"):
        self.dbname = database
        self.host_IP = host_IP
        self.username = username
        self.password = pword
        self.conn = pymysql.connect(host=host_IP, user=username, password=pword, db=database, charset="utf8mb4")


class CreateTable:
    class __Column:

        def __init__(self, name, column_type, length, comment, isPrimary, constraints):

            self.name = name
            self.data_type = column_type
            self.length = length
            self.comment = comment
            self.isPrimary = isPrimary
            self.constraints = constraints

        def __repr__(self):

            return "{} \t {} \t {} \t {} \t {}".format(self.name, self.data_type, self.length,
                                                       self.comment, str(self.isPrimary))

        def __hash__(self):

            return hash(self.__repr__())

    def __init__(self, name: str = None, columns=None):

        self.name = name
        if columns is None:
            self.columns = []
        else:
            self.columns = columns

    def __repr__(self):

        return "Table Name: {} \n\nColumns: \n {}".format(self.name, "\n".join(str(col) for col in self.columns))

    # todo: add error check
    def add_column(self, name, column_type, column_length, comment="", isPrimary=False, constraints=None):
        """

        :param name:
        :param column_type:
        :param column_length:
        :param comment:
        :return:
        """

        if type(name) is not str:
            raise ValueError("Invalid input for column name: expected: String, got: {}".format(str(type(name))))

        if type(column_type) is not str:
            raise ValueError("Invalid input for column type: expected: String, got: {}".format(str(type(column_type))))

        new_col = CreateTable.__Column(name, column_type, column_length, comment, isPrimary, constraints)
        self.columns.append(new_col)

    def create_table(self, connection):
        """

        :param connection:
        :return:
        """

        sql = self.create_table_sql()
        try:
            with connection.cursor() as cur:
                cur.execute(sql)
                connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def create_table_sql(self):
        """

        :return:
        """

        if len(self.columns) == 0:
            return ""
        else:
            sql = "CREATE TABLE IF NOT EXISTS `{}` (".format(self.name)
            for col in self.columns:
                if col.isPrimary:
                    isPrimary = " PRIMARY KEY"
                else:
                    isPrimary = ""
                    
                if col.comment == "":
                    comment = ""
                else:
                    comment = " COMMENT '{}'".format(col.comment)

                if col.data_type in ["DATETIME", "text", "TEXT"]:
                    length = ""
                else:
                    length = "({})".format(col.length)
                
                if col.constraints is None:
                    constraints = ""
                else:
                    constraints = " " + col.constraints
                
                sql += "`{}` {}{}{}{}{}, ".format(col.name, col.data_type, length, constraints, isPrimary, comment)
            return sql[:-2] + ");"

    # todo: implement method for setting primary key
    def set_primary(self):
        pass


def build_condition(col, items, condition):
    output = ""
    for item in items[:-1]:
        output += "`{}` = '{}' {} ".format(col, item, condition)
    output += "`{}` = '{}' ".format(col, items[-1])
    return output


def data_fetch(col, table, condition="", limit=100, start=0, host_IP="192.168.164.15", database="raw", user_name="", password="", tail_condition=""):
    if len(user_name) > 0 and len(password) > 0:
        username = user_name
        pword = password
    elif host_IP.split(".")[-1] == "101":
        username = "lduan"
        pword = "52192"
    elif host_IP.split(".")[-1] == "11":
        username = "raw"
        pword = "raw"
    elif host_IP.split(".")[-1] == "15":
        username = "raw"
        pword = "raw"
    else:
        raise ModuleNotFoundError("Server IP not supported")

    if condition != "":
        condition = " WHERE " + condition

    if limit is None:
        limit = ""
    else:
        limit = " LIMIT {}, {}".format(start, limit)
    
    if tail_condition == "":
        pass
    else:
        tail_condition = " " + tail_condition
    
    conn = pymysql.connect(host=host_IP, user=username, password=pword, db=database, charset="utf8")
    with conn.cursor() as a:
        sql = "SELECT {} FROM {}{}{}{};".format(col, table, condition, tail_condition, limit)
        # print(sql)
        a.execute(sql)
        data = a.fetchall()
    return data


def row_count(table, condition="", host_IP="192.168.164.15", database="raw"):
    if host_IP.split(".")[-1] == "139":
        username = "lduan"
        pword = "52192"
    elif host_IP.split(".")[-1] == "11":
        username = "raw"
        pword = "raw"
    elif host_IP.split(".")[-1] == "15":
        username = "raw"
        pword = "raw"
    elif host_IP.split(".")[-1] == "101":
        username = "lduan"
        pword = "52192"
    else:
        raise ModuleNotFoundError("Server IP not supported")

    if condition != "":
        condition = " WHERE " + condition

    conn = pymysql.connect(host=host_IP, user=username, password=pword, db=database, charset="utf8")
    with conn.cursor() as a:
        sql = "SELECT COUNT(*) FROM {}{};".format(table, condition)
        # print(sql)
        a.execute(sql)
        count = a.fetchall()
    return int(count[0][0])


if __name__ == "__main__":
    _ = 1
# data = data_fetch("id", "wechat_essays")
# for item in data:
#     print(item)

# print(row_count("wechat_essays", host_IP="192.168.164.139", database="wechat_0"))
