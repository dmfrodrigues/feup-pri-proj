import urllib.parse

import sys
import csv, json

def urlencode(s):
    return urllib.parse.quote_plus(s)

def pathencode(s):
    return urlencode(s).replace("%28", "(").replace("%29", ")")

def filterRelationships(col, keys):
    l = col.split(";")
    l = [s for s in l if s in keys]
    return ";".join(l)

assert len(sys.argv) == 3

filtered_file = open(sys.argv[1], "r")
texts_file    = open(sys.argv[2], "r")

keys = set([s.strip() for s in texts_file.readlines()])

w = csv.writer(sys.stdout)

r = csv.reader(filtered_file)
columns = next(r)
celex_idx = columns.index("celex")
relationships_idx = columns.index("relationships")
legalbasis_idx = columns.index("legal_basis")
addressee_idx = columns.index("addressee")
columns.append("text")
w.writerow(columns)

i = 0
for row in r:
    celex = row[celex_idx]
    if i%100 == 0:
        print(f"Processing {celex} (#{i})", file=sys.stderr)
    if celex in keys:
        f = open(f"eurlex/texts/{pathencode(celex)}.html", "r")
        s = f.read()
        f.close()
        while "\n\n\n" in s: s = s.replace("\n\n\n", "\n\n")
        s = s.replace(u'\u00A0', ' ')
        row.append(s)

        row[relationships_idx] = filterRelationships(row[relationships_idx], keys)
        row[legalbasis_idx] = filterRelationships(row[legalbasis_idx], keys)

        w.writerow(row)
    i += 1

filtered_file.close()
texts_file.close()
