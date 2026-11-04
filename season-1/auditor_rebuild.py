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

def reason(b):
    if b.get('public', True) and not b.get('encrypted', False):
        return "public + unencrypted"
    elif b.get('public', True):
        return "public"
    elif not b.get('encrypted', False):
        return "unencrypted"
    else:
        return "no issues"

for b in buckets:
    verdict = classify(b)
    r = reason(b)
    
    if verdict == "CRITICAL":
        criticals.append(f"{b['name']} ({r})")
    elif verdict == "WARNING":
        warnings.append(f"{b['name']} ({r})")

for c in criticals:
    print(f"CRITICAL: {c}")

for w in warnings:
    print(f"WARNING: {w}")

print()
print("Checked", len(buckets), "buckets:", len(criticals), "critical(s),", len(warnings), "warning(s)")
