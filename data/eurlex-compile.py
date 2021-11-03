import sys
import json

data = json.load(sys.stdin)
keys = data.keys()
for key in keys:
    print("Processing " + key, file=sys.stderr)
    entry = data[key]
    filepath = "eurlex/{}.txt".format(key)
    with open(filepath, "r") as f:
        s = f.read()
        data[key]["text"] = s

print(json.dumps(data, sort_keys=True, indent=2))
