import sys
import json

try:
    with open("buckets_export.json") as file:
        data = json.load(file)
except FileNotFoundError:
    print("ERROR: Buckets data not found. Please make sure the file is in the correct file location and try again.")
    sys.exit(1)

criticals = []
warnings = []

acc_name = data.get('account', {})
buckets = data.get('buckets', {})

print("Account:", acc_name)

def check_risk(b):
    name = b.get('name', "unknown")
    public = b.get('config', {}).get('public_access', {}).get('enabled', True)
    encrypted = b.get('config', {}).get('encryption', {}).get('enabled', False)
    owner = b.get('tags', {}).get('owner', "unknown")   

    if public and not encrypted:
        criticals.append(f"CRITICAL: {name} (public + unencrypted) [owner: {owner}]")
    elif public or not encrypted:
        if not encrypted:
            warnings.append(f"WARNING: {name} (unencrypted) [owner: {owner}]")
        else:
            warnings.append(f"WARNING: {name} (public) [owner: {owner}]")

for b in buckets:
    check_risk(b)

for c in criticals:
    print(c)

for w in warnings:
    print(w)

print()
print(f"Checked {len(buckets)} buckets: {len(criticals)} critical(s), {len(warnings)} warning(s)")
