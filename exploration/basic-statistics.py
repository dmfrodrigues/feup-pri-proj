import sys
import csv

csv.field_size_limit(sys.maxsize)

def avg(l: list) -> float:
    return sum(l)/len(l)

f = open("../data/eurlex/combined.csv", "r")
r = csv.reader(f, quotechar="'")

columns = next(r)
celex_idx = columns.index("celex")

data = dict()
for row in r:
    data[row[celex_idx]] = dict()
    for i in range(len(columns)):
        data[row[celex_idx]][columns[i]] = row[i]

print(f"Number of entries: {len(data)}")

form_dict = dict()
for entry in data.values():
    form = entry["form"]
    if not form in form_dict:
        form_dict[form] = 0
    form_dict[form] += 1

print("form:")
for form, count in form_dict.items():
    print(f"    '{form}': {count}")

print("date:")
m = min([entry["date"] for entry in data.values() if entry["date"] != ""]); print(f"    min: {m}")
m = max([entry["date"] for entry in data.values() if entry["date"] != ""]); print(f"    max: {m}")
m = len([entry["date"] for entry in data.values() if entry["date"] == ""]); print(f"    missing: {m}")

print("title:")
m = min([len(entry["title"]) for entry in data.values() if entry["title"] != ""]); print(f"    min size: {m}")
m = max([len(entry["title"]) for entry in data.values() if entry["title"] != ""]); print(f"    max size: {m}")
m = avg([len(entry["title"]) for entry in data.values() if entry["title"] != ""]); print(f"    avg size: {m}")
m = len([entry["title"] for entry in data.values() if entry["title"] == ""]); print(f"    missing: {m}")

print("oj_date:")
m = min([entry["oj_date"] for entry in data.values() if entry["oj_date"] != ""]); print(f"    min: {m}")
m = max([entry["oj_date"] for entry in data.values() if entry["oj_date"] != ""]); print(f"    max: {m}")
m = len([entry["oj_date"] for entry in data.values() if entry["oj_date"] == ""]); print(f"    missing: {m}")

print("of_effect:")
m = min([entry["of_effect"] for entry in data.values() if entry["of_effect"] != ""]); print(f"    min: {m}")
m = max([entry["of_effect"] for entry in data.values() if entry["of_effect"] != ""]); print(f"    max: {m}")
m = len([entry["of_effect"] for entry in data.values() if entry["of_effect"] == ""]); print(f"    missing: {m}")

print("end_validity:")
m = min([entry["end_validity"] for entry in data.values() if entry["end_validity"] != ""]); print(f"    min: {m}")
m = max([entry["end_validity"] for entry in data.values() if entry["end_validity"] != ""]); print(f"    max: {m}")
m = len([entry["end_validity"] for entry in data.values() if entry["end_validity"] == ""]); print(f"    missing: {m}")
