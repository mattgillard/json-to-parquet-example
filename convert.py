import json

with open("out.json", 'r') as j:
    contents=json.loads(j.read())
with open('output.jsonl', 'w') as outfile:
    for entry in contents:
        json.dump(entry, outfile)
        outfile.write('\n')
