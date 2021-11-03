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
                print("Processing {} ({})".format(content["celex"], content["date"]), file=sys.stderr)
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

def urlencode(s):
    return urllib.parse.quote_plus(s)

def pathencode(s):
    return urlencode(s).replace("%28", "(").replace("%29", ")")

def get_text(entry):
    celex = entry["celex"]
    filepath = "eurlex/texts/{}.txt".format(pathencode(celex))
    if os.path.exists(filepath):
        print("File already exists: {}".format(celex), file=sys.stderr)
        return entry
    else:
        text_url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{}".format(urlencode(celex))
        text = get_text_from_url(text_url)
        if text != None:
            f = open(filepath, 'w')
            f.write(text)
            print("Wrote: {}".format(celex), file=sys.stderr)
            entry["text_url"] = text_url
            return entry
            
        print("Problem raised: {}, url={}".format(celex, text_url), file=sys.stderr)
        return None
    return None

r = csv.reader(sys.stdin)
columns = next(r)

# print(columns, file=sys.stderr)

data = dict()
for row in r:
    # print(row, file=sys.stderr)    
    entry = dict()
    for col in columns:
        entry[col] = row[columns.index(col)]
    data[entry["celex"]] = entry

keys = list(data.keys())
keys.sort(reverse=True)

# data = [data[key] for key in keys if data[key]["date"] >= "2010-01-01" and not os.path.exists("eurlex/texts/{}.txt".format(urlencode(key)))]
data = list(data.values())

results = get_texts_parallel(data, 8)

out = dict()
for entry in results:
    if entry == None:
        continue
    key = entry["celex"]
    out[key] = entry

w = csv.writer(sys.stdout)
w.writerow(columns)
for celex, entry in out:
    w.writerow([entry[col] for col in columns])
