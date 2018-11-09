import json
import operator
import pickle
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
from pymysql.err import IntegrityError

from nlp.tf_idf.tf_idf import tfidf
from szqj.authors_networking.account_networking import Networks, Media, Relationship
from utils.mysql import data_fetch, Database


class LoadNetworks:

    def __init__(self):
        g = Networks()
        count = 0
        relationships = data_fetch("`id`, `media_id`, `src_media_id`", "media_media", limit=99999, host_IP="10.0.0.101",
                                   database="processing")
        for item in relationships:
            if item[1] == item[2]:
                count += 1
            else:

                media1 = Media(item[1])
                media2 = Media(item[2])
                g.add_media(media1)
                g.add_media(media2)
                g.add_relationship(Relationship(media1, media2, item[0]))


# initialize our web app object
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)
with open("../../data/nlp/idf.pickle", "rb") as file:
    idf = pickle.load(file)
connection = Database().conn


@app.route('/')
def index():
    """
    defining the welcome page
    :return:
    """
    return '<p>Welcome</p>' \
           '<p></p>'


@app.route("/essays/tfidf/", methods=["POST"])
def essay_tfidf():
    """
    
    :return: 
    """
    
    try:
        data = json.loads(request.data)
        eid = data["essay_id"]
        limit = int(data["limit"])
        method = int(data["method"])
    except Exception as e:
        return json.dumps({'code': 0, 'msg': 'FAILURE', 'data': {'error_msg': str(e)}})

    if limit <= 50:
        try:
            data = data_fetch("`content`", "essay_keywords", database="processing",
                              host_IP="10.0.0.101", condition="`essay_id`='{}'".format(eid),
                              user_name="lduan", password="52192")
            if len(data) == 0:
                pass
            else:
                content_dic = json.loads(data[0][0], encoding="utf8")
                ll = list(content_dic.items())
                ll.sort(key=operator.itemgetter(1), reverse=True)
                tops = ll[:min(limit, len(ll))]
                output = {}
                for item in tops:
                    output[item[0]] = item[1]
                return json.dumps({'code': 1, 'msg': 'SUCCESS', 'data': output}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 0, 'msg': 'FAILURE', 'data': {'error_msg': str(e)}})

    try:
        essay, pubdate = data_fetch("`content`, `pubdate`", "essays", condition="`id` = '{}'".format(eid),
                                    host_IP="192.168.164.15", user_name="raw", password="raw",
                                    database="raw")[0]

        result, fifty = tfidf(essay, idf, limit, method=method)
    except Exception as e:
        return json.dumps({'code': 0, 'msg': 'FAILURE', 'data': {'error_msg': str(e)}})

    sql_cols = """`essay_id`, `content`, `pubdate`, `insert_time`"""
    sql_values = """VALUES ('{}', '{}', '{}', '{}');""".format(
        eid,
        json.dumps(fifty, ensure_ascii=False),
        pubdate,
        datetime.now().replace(microsecond=0))

    sql = """INSERT INTO `essay_keywords` ({}) {}""".format(sql_cols, sql_values)
    try:
        with connection.cursor() as cur:
            cur.execute(sql)
            connection.commit()

        return json.dumps({'code': 1, 'msg': 'SUCCESS', 'data': result})
    except IntegrityError as e:
        if e.args[0] == 1062:
            return json.dumps({'code': 1, 'msg': 'SUCCESS', 'data': result})
        else:
            raise
    except Exception as e:
        return json.dumps({'code': 0, 'msg': 'FAILURE', 'data': {'error_msg': str(e)}})


@app.route("/user/network_rating", methods=["POST"])
def ntwk_rating():
    """
    
    :return: 
    """
    
    try:
        data = json.loads(request.data)
        mids = data["medias"]

    # 处理报错，直接返回失败并在data中附带错误信息
    except Exception as e:
        return json.dumps({'code': 0, 'msg': 'FAILURE', 'data': {'error_msg': str(e)}})
    
    relations = data_fetch("")


# 运行则开启服务对全网公开，端口51001
if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=51001)


