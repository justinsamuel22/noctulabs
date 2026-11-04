import json

with open("buckets.json") as file:
    buckets = json.load(file)

criticals = []
warnings = []

def classify(b):
    if b.get('public', True) and not b.get('encrypted', False):
        return "CRITICAL"
    elif b.get('public', True) or not b.get('encrypted', False):
        return "WARNING"
    else:
        return "OK"

for b in buckets:
    verdict = classify(b)

    if verdict == "CRITICAL":
        criticals.append(b['name'])
    elif verdict == "WARNING":
        warnings.append(b['name'])

for c in criticals:
    print("CRITICAL:", c)

for w in warnings:
    print("WARNING:", w)

print()
print("Checked", len(buckets), "buckets:", len(criticals), "critical(s),", len(warnings), "warning(s)")
