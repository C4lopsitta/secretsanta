import json
import os
import threading
import queue
from datetime import datetime

from SantaEntry import SantaEntry

writer_semaphore = threading.Semaphore(1)
writer_queue = queue.Queue()


def add_santa_entry(entry: SantaEntry):
    writer_queue.put(entry)


def create_new_store(store_id: str,
                     end_date: datetime,
                     deny_pairs: list[dict] = []):
    with open("santastores/"+store_id+".json", "w") as store:
        data = json.dumps({
            "people": [],
            "deny_pairs": deny_pairs,
            "end_date": end_date.isoformat()
        })
        store.write(data)


def delete_store(store_id: str):
    os.remove("santastores/"+store_id+".json")


def load_store(store_id: str) -> dict:
    return json.load(open("santastores/"+store_id+".json"))


def _writer(entry: SantaEntry):
    with writer_semaphore:
        with open("santastores/"+entry.store_id+".json", "r") as f:
            santa_list = json.load(f)

        santa_list["people"].append(entry.to_dict())

        with open("santastores/"+entry.store_id+".json", "w") as f:
            data = json.dumps(santa_list)
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

