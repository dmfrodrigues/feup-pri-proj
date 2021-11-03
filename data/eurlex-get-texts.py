"""
Processes eurlex/document-raw.json and finds urls for documents that do not have
a text_url supplied by api.epdb.eu
"""

import sys, json

import time
import os.path

from bs4 import BeautifulSoup

import queue
import urllib.request
from threading import Thread

def get_texts_parallel(entries, no_workers):
    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.results = []

            self.start_time = time.time()
            self.start_size = self.queue.qsize()

        def run(self):
            while True:
                content = self.queue.get()
                if content == "":
                    break
                print("Processing {} ({})".format(content["doc_id"], content["date_document"]), file=sys.stderr)
                entry = get_text(content)
                self.results.append(entry)
                self.queue.task_done()

                now_time = time.time()
                dt = now_time - self.start_time
                size = self.queue.qsize()
                dsize = size - self.start_size
                if dsize < 0:
                    dt1 = dt/(-dsize)
                    print("ETA {:.2f} seconds".format(dt1 * size), file=sys.stderr)

    # Create queue and add entries
    q = queue.Queue()
    for entry in entries:
        q.put(entry)

    # Create workers and add tot the queue
    workers = []
    for _ in range(no_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)
    # Workers keep working till they receive an empty string
    for _ in workers:
        q.put("")
    # Join workers to wait till they finished
    for worker in workers:
        worker.join()

    # Combine results from all workers
    r = []
    for worker in workers:
        r.extend(worker.results)
    return r

def get_text_from_url(text_url):
    try:
        response = urllib.request.urlopen(text_url)
    except:
        return None
    s = response.read()
    soup = BeautifulSoup(s, features="html.parser")
    # textEl = soup.find(id="TexteOnly")
    # if textEl != None: return textEl.get_text('\n').strip()
    # textEl = soup.find(id="docHtml")
    # print(soup)
    # if textEl != None: return textEl.get_text('\n').strip()
    return soup.get_text('\n').strip()

def get_text(entry):
    key = entry["doc_id"]
    text_url = entry["text_url"]
    filepath = "eurlex/{}.txt".format(key)
    if text_url != "":
        if os.path.exists(filepath):
            print("File already exists: {}".format(key), file=sys.stderr)
            return entry
        else:
            text_url = entry["eurlex_perma_url"].replace("http://eur-lex.europa.eu/LexUriServ/LexUriServ.do", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/").replace(":EN:NOT", "")
            text = get_text_from_url(text_url)
            if text != None:
                f = open(filepath, 'w')
                f.write(text)
                print("Wrote: {}".format(key), file=sys.stderr)
                entry["text_url"] = text_url
                return entry
                
            print("Problem raised: {}, url={}".format(key, text_url), file=sys.stderr)
            return None
    return None

data = json.load(sys.stdin)
keys = list(data.keys())
keys.sort(reverse=True)
# data = [data[key] for key in keys if data[key]["date_document"] >= "1950-01-01" and not os.path.exists("eurlex/{}.txt".format(key))]
data = list(data.values())

results = get_texts_parallel(data, 8)

out = dict()
for entry in results:
    if entry == None:
        continue
    key = entry["doc_id"]
    out[key] = entry
print(json.dumps(out, sort_keys=True, indent=2))
