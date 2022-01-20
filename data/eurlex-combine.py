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
ranked_file   = open(sys.argv[2], "r")

ranks = dict()
r = csv.reader(ranked_file)
next(r)
for row in r:
    celex, rank = row
    ranks[celex] = rank
ranked_file.close()
keys = ranks.keys()

r = csv.reader(filtered_file)
w = csv.writer(sys.stdout)
columns = next(r)
celex_idx = columns.index("celex")
legal_basis_idx = columns.index("legal_basis")
relationships_idx = columns.index("relationships")
columns.append("rank")
columns.append("text")
w.writerow(columns)

i = 0
for row in r:
    celex = row[celex_idx]
    if i%100 == 0:
        print(f"Processing {celex} (#{i})", file=sys.stderr)
    if celex in ranks:
        f = open(f"eurlex/texts/{pathencode(celex)}.html", "r")
        text = f.read()
        f.close()
        # text = text.replace(u'\u00A0', ' ')

        row[legal_basis_idx  ] = ";".join([i for i in row[legal_basis_idx  ].split(";") if i in keys])
        row[relationships_idx] = ";".join([i for i in row[relationships_idx].split(";") if i in keys])
        
        row.append(ranks[celex])
        row.append(text)

        w.writerow(row)
    i += 1

filtered_file.close()

