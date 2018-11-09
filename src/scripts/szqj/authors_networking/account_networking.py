import pickle
import warnings
from datetime import datetime

import requests
from pymysql import IntegrityError

from utils.mysql import data_fetch
from utils.read_txt import read_txt
from utils.text_cleaner import html_cleanup
from utils.text_utilizer import get_md5, re_between_findall, remove_punctuation
# from utils.web_utilizer import SogouWeixin


class Media:
    """
    Media class
    """

    def __init__(self, media_id):
        """
        Initialize Media object, takes in 2 points as input
        :param name: Media name
        """

        self.id = media_id
        # self.nick = nick
        # self.platform_id = platform_id

    def __repr__(self):
        return "Media: {}".format(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.__repr__())


class Relationship:
    """
    Relationship class
    """

    def __init__(self, account1: Media, account2: Media, r_id="Unknown", weight=0, r_type="转载"):
        """
        Initialize Relationship object, takes in 2 points as input
        :param p1: point1
        :param p2: point2
        :param dist: distance, default 1
        """

        # Check for input type
        if type(account1) is not Media:
            if type(account2) is not Media:
                raise TypeError("Invalid input type for p1: '{}' and p2: {}. "
                                "Expecting '{}'".format(type(account1), type(account2), Media))
            else:
                raise TypeError("Invalid input type for p1: '{}'"
                                "Expecting '{}'".format(type(account1), Media))
        else:
            if type(account2) is not Media:
                raise TypeError("Invalid input type for p2: {}. "
                                "Expecting '{}'".format(type(account2), Media))

        self.point1 = account1
        self.point2 = account2
        self.r_id = r_id
        # self.essay_id = essay_id
        # self.essay_pubdate = essay_pubdate
        # self.insert_time = insert_time
        self.r_type = r_type

        # distance of point1 and point2
        self.distance = self._get_distance(weight)
        self.weight = weight

    def __repr__(self):
        return "Relationship: {}--{} \n".format(self.point1.id, self.point2.id)

    def __eq__(self, other):
        points_chk = self.point1 == other.point1 and self.point2 == other.point2
        dist_chk = self.distance == other.distance
        return points_chk and dist_chk

    def __hash__(self):
        return hash(self.__repr__())

    def __contains__(self, item):
        if type(item) is not Media:
            return False
        return self.point1 == item or self.point2 == item

    def _get_distance(self, dist):
        """
        check dist parameter to see if input is valid
        :param dist: distance input
        :return: processed distance input
        """

        if dist is None:
            dist = 1
            default = True
        else:
            default = False

        if self.point1 == self.point2:
            if default:
                return 0
            else:
                raise ValueError("Distance 'between' one single point should be 0, {} given.".format(dist))
        else:
            return dist


class Networks:
    """
    Networks class
    """

    def __init__(self, vertices: [Media] = [], edges: [Relationship] = []):
        """
        Basic data structure
        """

        self.vertices, self.edges = self._check_inputs_property(vertices, edges)

    def __repr__(self):
        return "Vertices: {}; \n Edges: {}".format(str(self.vertices), str(self.edges))

    def __eq__(self, other):
        return set(self.edges) == set(other.edges) and set(self.vertices) == set(other.vertices)

    def __hash__(self):
        return hash(self.__repr__())

    def __contains__(self, item):
        if type(item) is Media:
            return item in self.vertices
        elif type(item) is Relationship:
            return item in self.edges
        else:
            return False

    def is_connected(self, vertex_1: Media, vertex_2: Media):
        """
        check if 2 points are connected
        :param vertex_1: 1st vertex object
        :param vertex_2: 2nd vertex object
        :return: boolean
        """

        # check if the given points are in the graph
        if vertex_1 in self.vertices:
            if vertex_2 in self.vertices:
                return Relationship(vertex_1, vertex_2) in self.edges
            else:
                warnings.warn("Media 2 is not in the graph! ")
                return False
        else:
            warnings.warn("Media 1 is not in the graph! ")
            return False

    @staticmethod
    def _check_inputs_type(vertices, edges):
        """
        check if inputs are valid
        :param vertices: input vertices list
        :param edges: input edges list
        :return: checked vertices list and edges list
        """

        # checking data type
        if not all(isinstance(item, Media) for item in vertices):
            raise TypeError("Invalid type for vertices input!")
        if not all(isinstance(item, Relationship) for item in edges):
            raise TypeError("Invalid type for edges input!")

    @staticmethod
    def _check_inputs_property(vertices, edges):
        # checking completeness
        vertices_temp = set()
        for item in edges:
            vertices_temp.add(item.point1)
            vertices_temp.add(item.point2)
        if len(vertices_temp) > len(vertices):
            warnings.warn("Vertices given is not complete. Will automatically add vertices those are "
                          "present in edges but not in vertices.")
            vertices = list(vertices_temp)

        # checking duplicates
        vertices_set = set(vertices)
        if len(vertices_set) < len(vertices):
            warnings.warn("Duplicated vertices found! Total: {}".format(len(vertices) - len(vertices_set)))
        edges_set = set(edges)
        if len(edges_set) < len(edges):
            warnings.warn("Duplicated vertices found! Total: {}".format(len(edges) - len(edges_set)))
        return list(vertices_set), list(edges_set)

    def add_media(self, vert: Media):
        if vert not in self.vertices:
            self.vertices.append(vert)

    def add_relationship(self, edge: Relationship):
        if edge not in self.edges:
            self.edges.append(edge)

    def connected_vertices(self, media):
        output = []
        for edge in self.edges:
            if media in edge:
                output.append(media)
        return output


class Essay:

    def __init__(self, raw):
        self.platform_id = raw[0]
        self.platform = raw[1]
        self.media_id = raw[2]
        self.media_nick = raw[3]
        self.media_name = raw[4]
        self.media_src_id = raw[5]
        self.src_id = raw[6]
        self.f_id_scale = raw[7]
        self.title = raw[8]
        self.meta_content = raw[9]
        self.pubdate = raw[10]
        self.images = raw[11]
        self.content = raw[12]
        self.view_count = raw[13]
        self.like_count = raw[14]
        self.fav_count = raw[15]
        self.comment_count = raw[16]
        self.forward_count = raw[17]
        self.id = raw[18]
        self.insert_time = raw[19]
        self.update_time = raw[20]

    def author_from_meta(self):
        if self.meta_content is None:
            self.meta_content = ""
        authors = self.meta_content.split(" ")
        essay_authors = []
        essay_type = ""
        account_name = ""
        if len(authors) > 1:
            if "点关注" in authors[0]:
                authors = authors[1:]

            if "原创" in authors[0]:
                essay_type = authors[0][:2]
                if len(authors) == 2:
                    essay_authors = [authors[0].replace("原创：", "")]
                else:
                    essay_authors = [authors[0][3:]]
                    essay_authors += authors[1:-1]
            else:
                essay_type = "不详"
                if len(authors) == 2:
                    essay_authors = [authors[0].replace("原创：", "")]
                else:
                    essay_authors = [authors[0]]
                    essay_authors += authors[1:-1]

            account_name = authors[-1]
        else:
            account_name = authors[0]
        # print(authors)
        # print("authors: {} \n account_name: {} \n type: {} \n".format(str(essay_authors), account_name, essay_type))
        return essay_authors, account_name, essay_type

    def author_relation_id_generator(self, author_name):
        return get_md5("{}-{}-{}-{}".format(self.platform_id, author_name, self.media_id, self.id))

    def media_relation_id_generator(self, src_id):
        return get_md5("{}-{}-{}-{}".format(self.platform, self.media_id, src_id, self.id))

    def meta_author_insert(self, connection):
        essay_authors, account_name, essay_type = self.author_from_meta()
        if len(essay_authors) == 0:
            return 0
        else:
            count = 0
            for author in essay_authors:
                sql_cols = """`id`, `name`, `media_id`, `media_nick`, `platform_id`, `essay_id`, `essay_pubdate`, `insert_time`"""
                sql_values = """VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                    self.author_relation_id_generator(author),
                    author,
                    self.media_id,
                    self.media_nick,
                    self.platform_id,
                    self.id,
                    self.pubdate,
                    datetime.now().replace(microsecond=0))
                sql = """INSERT INTO `author_media` ({}) {}""".format(sql_cols, sql_values)

                try:
                    with connection.cursor() as cur:
                        # print(sql)
                        cur.execute(sql)
                        connection.commit()
                    count += 1
                except IntegrityError as e:
                    # print(e.args)
                    if e.args[0] == 1062:
                        pass
                    else:
                        print(e)
                except Exception as e:
                    print(e)
                    # return False
            return count

    def info_extract(self):
        content = self.content
        account_associate_rules = read_txt("../../../../data/nlp/essay_author/account_associate_rules.txt")
        author_associate_rules = read_txt("../../../../data/nlp/essay_author/author_associate_rules.txt")
        author_blklist = read_txt("../../../../data/nlp/essay_author/author_blklist.txt")
        account_blklist = read_txt("../../../../data/nlp/essay_author/account_blklist.txt")
        count = 0
        media_list = []
        author_list = []
        if content is not None:
            content = html_cleanup(content)
            for auth_rule in author_associate_rules:
                result = re_between_findall(content, auth_rule)
                if result is not None:
                    for item in result:
                        s = remove_punctuation(item[1], exception="、")
                        if s != "":
                            authors = s.split("、")
                            for auth in authors:
                                if len(auth) < 2:
                                    break
                                else:
                                    blk = 0
                                    for blk_item in author_blklist:
                                        if blk_item in auth:
                                            blk += 1
                                    if blk:
                                        pass
                                    else:
                                        count += 1
                                        author_list.append(auth)

            for acc_rule in account_associate_rules:
                result = re_between_findall(content, acc_rule)
                if result is not None:
                    for item in result:
                        s = remove_punctuation(item[1], exception="、")
                        if s != "":
                            medias = s.split("、")
                            for media in medias:
                                if len(media) < 2:
                                    break
                                else:
                                    # obj = SogouWeixin(media)
                                    # info = obj.extract_user_info()
                                    # print("What we found: {} \nWhat we got: {}".format(media, info["nickname"]))
                                    # if media == info["nickname"]:
                                    if len(media) > 7 and "、" not in media:
                                        pass
                                    else:
                                        blk = 0
                                        for blk_item in account_blklist:
                                            if blk_item in media:
                                                blk += 1
                                        if blk:
                                            pass
                                        else:
                                            count += 1
                                            media_list.append(media)
                                        # print(media.replace(" ", "").replace("文丨", ""))
        return [list(set(media_list)), list(set(author_list))]

    @staticmethod
    def examine_media(media_name):
        url = "http://10.0.0.22:4567/sogou/search/" + media_name
        response = requests.post(url)
        try:
            result = response.json()
        except Exception as e:
            print(response.text)
            print(e)
            return False

        if result["code"] == 211:
            return False
        elif result["code"] == 1:
            data = result["data"]
            for item in data:
                if item["nick"] == media_name:
                    return True
            return False

    def extractor_info_insert(self, connection):

        media_list, author_list = self.info_extract()
        media_count = 0
        author_count = 0
        # 媒体
        if len(media_list) > 0:
            for media in media_list:
                with open("../../../../data/szqj/medias.pickle", "rb") as f:
                    known_medias = pickle.load(f)
                if media in known_medias:
                    if self.media_nick == media:
                        pass
                    else:
                        src_id = get_md5(self.platform + "-" + media)
                        sql_cols = """`id`, `media_id`, `media_nick`, `platform_id`, `src_media_id`, `src_media_nick`, `type`, `essay_id`, `essay_pubdate`, `insert_time`"""
                        sql_values = """VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                            self.media_relation_id_generator(src_id),
                            self.media_id,
                            self.media_nick,
                            self.platform_id,
                            src_id,
                            media,
                            "转载",
                            self.id,
                            self.pubdate,
                            datetime.now().replace(microsecond=0))
                        sql = """INSERT INTO `media_media` ({}) {}""".format(sql_cols, sql_values)

                        try:
                            with connection.cursor() as cur:
                                # print(sql)
                                cur.execute(sql)
                                connection.commit()
                                media_count += 1
                        except IntegrityError as e:
                            # print(e.args)
                            if e.args[0] == 1062:
                                pass
                            else:
                                print(e)
                        except Exception as e:
                            print(e)
                else:
                    pass
                    # if self.examine_media(media):
                    #     known_medias.append(media)
                    #     
                    #     with open("../../../data/szqj/medias.pickle", "wb") as f:
                    #         pickle.dump(known_medias, f)
                    #     
                    #     try:
                    #         url = "http://10.0.0.22:4567/sogou/fetch/" + media
                    #         response = requests.post(url).json()
                    #         if response["code"] != 1:
                    #             print(response["msg"])
                    #     except Exception as e:
                    #         print(e)
                    #     
                    #     src_id = get_md5(self.platform + "-" + media)
                    #     sql_cols = """`id`, `media_id`, `media_nick`, `platform_id`, `src_media_id`, `src_media_nick`, `type`, `essay_id`, `essay_pubdate`, `insert_time`"""
                    #     sql_values = """VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                    #         self.media_relation_id_generator(src_id),
                    #         self.media_id,
                    #         self.media_nick,
                    #         self.platform_id,
                    #         src_id,
                    #         media,
                    #         "转载",
                    #         self.id,
                    #         self.pubdate,
                    #         datetime.now().replace(microsecond=0))
                    #     sql = """INSERT INTO `media_media` ({}) {}""".format(sql_cols, sql_values)
                    #     try:
                    #         with connection.cursor() as cur:
                    #             # print(sql)
                    #             cur.execute(sql)
                    #             connection.commit()
                    #             media_count += 1
                    #     except Exception as e:
                    #         print(e)
                    # else:
                    #     pass

        # 作者
        if len(author_list) > 0:
            for author in author_list:
                if len(author) > 1:
                    sql_cols = """`id`, `name`, `media_id`, `media_nick`, `platform_id`, `essay_id`, `essay_pubdate`, `method`, `insert_time`"""
                    sql_values = """VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                        self.author_relation_id_generator(author),
                        author,
                        self.media_id,
                        self.media_nick,
                        self.platform_id,
                        self.id,
                        self.pubdate,
                        "extract",
                        datetime.now().replace(microsecond=0))
                    sql = """INSERT INTO `author_media` ({}) {}""".format(sql_cols, sql_values)

                    try:
                        with connection.cursor() as cur:
                            # print(sql)
                            cur.execute(sql)
                            connection.commit()
                            author_count += 1
                    except IntegrityError as e:
                        # print(e.args)
                        if e.args[0] == 1062:
                            pass
                        else:
                            print(e)
                    except Exception as e:
                        print(e)
        return media_count, author_count


if __name__ == "__main__":
    _ = 1

    count = 0
    g = Networks()
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

    conn_count = {}
    for item in g.vertices:
        conn_count[item] = g.connected_vertices(item)
