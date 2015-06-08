import os
import json

testDataPath = '/Users/williraschkowski/Developer/knowledge-miners/scripts/testdata/'
paths = [os.path.join(testDataPath,fn) for fn in next(os.walk(testDataPath))[2] if fn.endswith('.json')]

columnCount = {}
tables = 0
keys = 0

for path in paths:
    with open(path, 'r') as f:
        try:
            table = json.load(f)
            tables += 1
        except Exception:
            continue

        for key in table.keys():
            keys += 1
            if key in columnCount:
                columnCount[key] += 1
            else:
                columnCount[key] = 1

import operator
sorted_x = sorted(columnCount.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x)

print(keys)
print(len(columnCount))
print(tables)

with open('/Users/williraschkowski/Developer/knowledge-miners/data/keys.json', 'w') as f:
    json.dump({
        'tables': tables,
        'keys': keys,
        'keys (distinct)': len(columnCount),
        'occurances': sorted_x
    }, f)