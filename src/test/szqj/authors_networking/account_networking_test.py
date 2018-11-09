import multiprocessing as mp

from szqj.authors_networking.account_networking import *
from utils.mysql import data_fetch, Database, row_count


def update_author_networking_from_meta():
    start = 0
    db = Database()
    total = int(data_fetch("COUNT(*)", "essays", start=start, limit=None)[0][0])
    scan_count = start
    insert_count = 0
    limit = 10000

    while scan_count < total:

        if limit > total - scan_count:
            limit = total - scan_count

        data = data_fetch("*", "essays", start=start, limit=limit)

        for raw_item in data:
            obj = Essay(raw_item)
            response = obj.author_insert(db.conn)
            scan_count += 1
            if response:
                insert_count += response

            if scan_count % 1000 == 0:
                print(
                    "Scanned {} out of {} essays \n Inserted {} relation \n \n".format(scan_count, total, insert_count))
        start += limit


def worker(w_id, start, end):
    print("===============Process {} has started================".format(w_id))

    db = Database()
    total = end
    scan_count = 0
    limit = 10000
    chunk_size = end - start

    media_inserted = 0
    author_inserted = 0

    while scan_count < (end - start):

        if limit > total - scan_count - start:
            limit = total - scan_count - start

        data = data_fetch("*", "essays", start=start, limit=limit, tail_condition="ORDER BY `insert_time` DESC")

        for raw_item in data:
            obj = Essay(raw_item)
            media_count, author_count = obj.extractor_info_insert(db.conn)
            author_count += obj.meta_author_insert(db.conn)
            scan_count += 1
            if media_count + author_count:
                media_inserted += media_count
                author_inserted += author_count

            if scan_count % 1000 == 0:
                print(
                    "Process {} has scanned {} out of {} essays \n Inserted {} author relations \n Inserted {} media relations\n".format(
                        w_id, scan_count, chunk_size, author_inserted, media_inserted))
        start += limit
    print("===============Process {} has ended================".format(w_id))


if __name__ == "__main__":
    _ = 1

    num = row_count("essays", host_IP="192.168.164.15", database="raw")

    manager = mp.Manager()
    items = manager.list()

    process_num = 2
    inputs = []
    start_ind = 0
    chunk = int((num - start_ind) / process_num)

    for i in range(process_num):
        inputs.append((start_ind, start_ind + chunk))
        start_ind += chunk + 1
    print(inputs)
    counter = 0
    processes = []
    for input1, input2 in inputs:
        processes.append(mp.Process(target=worker, args=(counter, input1, input2,)))
        counter += 1

    # 运行所有进程
    for p in processes:
        p.start()

    # 确定所有进程结束
    for p in processes:
        p.join()
