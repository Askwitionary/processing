from utils.mysql import data_fetch, build_condition

id_list = ['2462acae8ed692945720e6acf6825c56',
           'c0b0b4d041856d52c0c4c97adf8a5985',
           'f365ff75ae3c3b39d7dd5f0b9335ed3a',
           'd4fa139b651f9efc5b5298a58e89f0ee',
           '54bf7dea08ac923ad6cb9bf894d50013',
           '036519b7296d1e5b0273e354cd310c06',
           '138df8b28925617a759e425c63e7f642',
           '6d4c13d26a41d6fc6c57d5c2aa652616',
           '9a6079cfa40e89c923754d677d2a586e',
           '26eb934f3637b266c44f2b2f46f5df2a']

nick_list = ['北京女主',
             '马铃薯精英网',
             '毕节市银行卡协会',
             '一诺法鼎财税',
             '财经野史',
             '独区企业服务平台',
             '每日股市秘闻',
             '融邦投资',
             '营销案例分析',
             '大安热线']

data_from_media = data_fetch("`media_id`, `media_nick`, `src_media_id`, `src_media_nick`, `type`, `essay_id`",
                             "media_media",
                             condition=build_condition("media_id", id_list, "OR"),
                             limit=None,
                             host_IP="10.0.0.101",
                             database="processing")

data_from_src = data_fetch("`media_id`, `media_nick`, `src_media_id`, `src_media_nick`, `type`, `essay_id`",
                           "media_media",
                           condition=build_condition("src_media_id", id_list, "OR"),
                           limit=None,
                           host_IP="10.0.0.101",
                           database="processing")

if __name__ == "__main__":
    _ = 1
