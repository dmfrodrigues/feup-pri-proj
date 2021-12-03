import sys, csv

r = csv.reader(sys.stdin, quotechar="'")
w = csv.writer(sys.stdout, quotechar="'")

columns = next(r)
w.writerow(columns)

date_idx = columns.index("date")

for row in r:
    date = row[date_idx]
    if date != "" and date < "1965-01-01":
        w.writerow(row)
