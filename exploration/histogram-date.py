import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

import csv

f = open("../data/eurlex/filtered.csv", "r")
r = csv.reader(f, quotechar="'")
columns = next(r)
celex_idx = columns.index("celex")
date_idx = columns.index("date")

dates = []
mpl_dates = []

no_date = 0
for row in r:
    d = row[date_idx]
    d2 = row[ojdate_idx]
    if d != "":
        dates.append(d)
        mpl_dates.append(mdates.datestr2num(d))
    else:
        no_date += 1

print(f'Failed to find date for {no_date} documents', file=sys.stderr)

print(f'min={min(dates)}')
print(f'max={max(dates)}')

# the histogram of the data
fig, ax = plt.subplots(1,1)
plt.grid(linestyle='dashed', axis="x", color=(0, 0, 0, 0.25), zorder=-1)
plt.grid(linestyle='dashed', axis="y", color=(0, 0, 0, 0.25), zorder=1)
ax.hist(mpl_dates, bins=65, edgecolor='black', linewidth=0.5, range=(mdates.datestr2num("1949-01-01"), mdates.datestr2num("2014-01-01")), zorder=0)
ax.xaxis.set_major_locator(mdates.YearLocator(5))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_xlim([datetime.date(1949, 1, 1), datetime.date(2014, 1, 1)])
ax.set_ylim([0, 5000])
plt.xticks(rotation=90)
plt.yticks(range(0, 5001, 500))
plt.show()
