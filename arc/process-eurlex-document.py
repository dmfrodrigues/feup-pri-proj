"""
Processes eurlex/document-raw.json and finds urls for documents that do not have
a text_url supplied by api.epdb.eu
"""

import sys, json

import time

from bs4 import BeautifulSoup

import queue
import urllib.request
from threading import Thread

def perform_fixing(entries, no_workers):
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
                # print("Processing " + content["doc_id"], file=sys.stderr)
                entry = fix_text_url(content)
                self.results.append(entry)
                self.queue.task_done()

                now_time = time.time()
                dt = now_time - self.start_time
                size = self.queue.qsize()
                dsize = size - self.start_size
                dt1 = dt/(-dsize)
                print("ETA {:.2f} seconds".format(dt1 * size))

    # Create queue and add entries
    q = queue.Queue()
    for key in entries.keys():
        q.put(entries[key])

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

LANGUAGES = ["EN", "FR", "DE", "IT", "NE"]

def try_text_other_languages(entry):
    for language in LANGUAGES:
        eurlex_perma_url = entry["eurlex_perma_url"]
        text_url = eurlex_perma_url.replace(":EN:NOT", ":{}:HTML".format(language))
        try:
            response = urllib.request.urlopen(text_url)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                continue
            raise
        
        s = response.read()
        soup = BeautifulSoup(s, features="html.parser")
        textEl = soup.find(id="TexteOnly")
        if textEl != None:
            # print("    Found text for key " + entry["doc_id"] + ", url=" + text_url, file=sys.stderr)
            return text_url
        errorEl = soup.find(id="errorDocumentView")
        if errorEl != None:
            continue

        # print("    TEXT PANIC! key " + entry["doc_id"] + ", url=" + text_url, file=sys.stderr)
        return text_url
    return None

def try_pdf_other_languages(entry):
    for language in LANGUAGES:
        eurlex_perma_url = entry["eurlex_perma_url"]
        pdf_url = eurlex_perma_url.replace("http://eur-lex.europa.eu/LexUriServ/LexUriServ.do", "https://eur-lex.europa.eu/legal-content/{}/TXT/PDF/".format(language)).replace(":EN:NOT", "")
        try:
            response = urllib.request.urlopen(pdf_url)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                continue
            raise
        if response.headers.get("Content-Type").startswith("application/pdf"):
            # print("    Found PDF for key " + entry["doc_id"] + ", url=" + pdf_url, file=sys.stderr)
            return pdf_url
        s = response.read()
        soup = BeautifulSoup(s, features="html.parser")
        errorEl = soup.find(id="errorDocumentView")
        if errorEl != None:
            continue

        print("    PDF PANIC! key " + entry["doc_id"] + ", url=" + pdf_url, file=sys.stderr)

    return None

def fix_text_url(entry):
    key = entry["doc_id"]
    entry["pdf_url"] = ""
    if entry["text_url"] == "":
        print("Processing " + key, file=sys.stderr)

        url = try_text_other_languages(entry)
        if url != None:
            entry["text_url"] = url
            return entry

        url = try_pdf_other_languages(entry)
        if(url != None):
            entry["pdf_url"] = url
            return entry

        # print("    Failed to find text/pdf of key " + key + ", url=" + entry["eurlex_perma_url"], file=sys.stderr)

    return entry



data = json.load(sys.stdin)

d = perform_fixing(data, 8)

print(a)
