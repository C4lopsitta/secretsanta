import json
import os
import threading
import queue
from datetime import datetime

import cron_handler
from SantaEntry import SantaEntry

writer_semaphore = threading.Semaphore(1)
writer_queue = queue.Queue()


def add_santa_entry(entry: SantaEntry):
    writer_queue.put(entry)


def create_new_store(store_id: str,
                     end_date: datetime,
                     deny_pairs: list[dict] = []):
    with open("santastores/" + store_id + ".json", "w") as store:
        data = json.dumps({
            "people": [],
            "deny_pairs": deny_pairs,
            "end_date": end_date.isoformat()
        })
        store.write(data)


def delete_store(store_id: str):
    os.remove("santastores/" + store_id + ".json")


def load_store(store_id: str) -> dict:
    store = json.load(open("santastores/" + store_id + ".json"))

    # if not store.keys().__contains__("cron_key"):
    #     try:
    #         cron_handler.add_cron(job_name=store_id,
    #                               curl_command="curl localhost:9091/",
    #                               date_time=datetime.fromisoformat(store["end_date"]))
    #     except Exception as e:
    #         print("[ERROR] " + e.__str__())
    #     # TODO)) Add cron process

    return store


def _writer(entry: SantaEntry):
    with writer_semaphore:
        with open("santastores/" + entry.store_id + ".json", "r") as f:
            santa_list = json.load(f)

        santa_list["people"].append(entry.to_dict())

        with open("santastores/" + entry.store_id + ".json", "w") as f:
            data = json.dumps(santa_list, indent=4)
            f.write(data)


def _process_write_requests():
    while True:
        entry = writer_queue.get()
        _writer(entry)
        writer_queue.task_done()


_worker = threading.Thread(target=_process_write_requests)
_worker.start()


def await_worker():
    _worker.join()
