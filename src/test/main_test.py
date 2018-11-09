import json

import requests


def essay_tfidf_test():
    url = "http://10.0.0.59:51001/essays/tfidf/"
    # url = "http://0.0.0.0:51001/essays/tfidf/"
    response = requests.post(url,
                             data=json.dumps({"essay_id": "834f1e658450f0389d3aa48090d5a31c", "limit": 50, "method": 1},
                                             ensure_ascii=False))
    data = response.json()
    print("Length: {}".format(len(data["data"])))
    return response


if __name__ == "__main__":
    _ = 1

    r1 = essay_tfidf_test()
