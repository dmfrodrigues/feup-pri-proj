"""
Processes eurlex/processed.csv and finds urls for documents that do not have
a text_url supplied by api.epdb.eu
"""

import sys, csv
csv.field_size_limit(sys.maxsize)

import time
import os.path

from bs4 import BeautifulSoup

import queue
import urllib.parse, urllib.request
from threading import Thread

import random

def get_texts_parallel(entries, no_workers):
    class Worker(Thread):
        def __init__(self, id, request_queue):
            Thread.__init__(self)
            self.id = id
            self.queue = request_queue
            self.results = []

            self.start_time = time.time()
            self.start_size = self.queue.qsize()

        def run(self):
            while True:
                content = self.queue.get()
                if content == "":
                    break
                # print("Processing {} ({})".format(content["celex"], content["date"]), file=sys.stderr)
                entry = get_text(content)
                self.results.append(entry)
                self.queue.task_done()

                now_time = time.time()
                dt = now_time - self.start_time
                size = self.queue.qsize()
                dsize = size - self.start_size
                if self.id == 0 and dsize < 0 and (-dsize)%1 == 0:
                    dt1 = dt/(-dsize)
                    print("ETA {:.2f} seconds".format(dt1 * size), file=sys.stderr)

    # Create queue and add entries
    q = queue.Queue()
    for entry in entries:
        q.put(entry)

    # Create workers and add tot the queue
    workers = []
    for i in range(no_workers):
        worker = Worker(i, q)
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
    # soup = BeautifulSoup(s, features="html.parser")
    # textEl = soup.find(id="TexteOnly")
    # if textEl != None: return textEl.get_text('\n').strip()
    # textEl = soup.find(id="docHtml")
    # print(soup)
    # if textEl != None: return textEl.get_text('\n').strip()
    # txt = soup.get_text('\n').strip()
    txt = s
    if txt.find(b"The requested document does not exist") != -1: return None
    # while "\n\n\n" in txt: txt = txt.replace("\n\n\n", "\n\n")
    return txt

def urlencode(s):
    return urllib.parse.quote_plus(s)

def pathencode(s):
    return urlencode(s).replace("%28", "(").replace("%29", ")")

def get_text(entry):
    celex = entry["celex"]
    filepath = "eurlex/texts/{}.html".format(pathencode(celex))
    filepath_notexts = "eurlex/notexts/{}.html".format(pathencode(celex))
    if os.path.exists(filepath):
        # print("File already exists: {}".format(celex), file=sys.stderr)
        return entry
    elif os.path.exists(filepath_notexts):
        # print("File already known not to exist: {}".format(celex), file=sys.stderr)
        return None
    else:
        text_url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{}".format(urlencode(celex))
        text = get_text_from_url(text_url)
        if text != None:
            f = open(filepath, 'wb')
            f.write(text)
            f.close()
            # print("Wrote: {}".format(celex), file=sys.stderr)
            entry["text_url"] = text_url
            return entry
            
        # print("Problem raised: {}, url={}".format(celex, text_url), file=sys.stderr)
        f = open(filepath_notexts, 'w')
        f.write("")
        f.close()
        return None
    return None

r = csv.reader(sys.stdin)
columns = next(r)

data = dict()
for row in r: 
    entry = dict()
    for col in columns:
        entry[col] = row[columns.index(col)]
    data[entry["celex"]] = entry

keys = list(data.keys())
keys.sort(reverse=True)

# data = [data[key] for key in keys if data[key]["date"] >= "2010-01-01" and not os.path.exists("eurlex/texts/{}.txt".format(urlencode(key)))]
data = list(data.values())
random.shuffle(data)

results = get_texts_parallel(data, 32)

keys = [entry['celex'] for entry in results if entry != None]
keys.sort()

for key in keys:
    print(key)
