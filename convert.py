import json

with open("features.json", 'r') as j:
    contents=json.loads(j.read())
with open('output.jsonl', 'w') as outfile:
    for entry in contents['features']:
        json.dump(entry, outfile)
        outfile.write('\n')
