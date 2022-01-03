import sys, csv

for line in sys.stdin:
    sys.stdout.write(line)

# r = csv.reader(sys.stdin)
# w = csv.writer(sys.stdout)

# columns = next(r)
# w.writerow(columns)

# date_idx = columns.index("date")

# for row in r:
#     date = row[date_idx]
#     if date != "" and date < "1965-01-01":
#         w.writerow(row)
