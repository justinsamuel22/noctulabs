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

report = []

acc_name = data.get('account', {})
buckets = data.get('buckets', {})

print("Account:", acc_name)

def check_risk(b):
    name = b.get('name', "unknown")
    public = b.get('config', {}).get('public_access', {}).get('enabled', True)
    encrypted = b.get('config', {}).get('encryption', {}).get('enabled', False)
    owner = b.get('tags', {}).get('owner', "unknown")   

    if public and not encrypted:
        reason = "public + unencrypted"
        report.append({"account":acc_name, "checked":len(data), "criticals":[{"name": f"{name}", "reason":f"{reason}", "owner":f"{owner}"}]})
        criticals.append(f"CRITICAL: {name} ({reason}) [owner: {owner}]")
    elif public or not encrypted:
        if not encrypted:
            reason = "unencrypted"
            report.append({"account":acc_name, "checked":len(data), "warnings":[{"name": f"{name}", "reason":f"{reason}", "owner":f"{owner}"}]})
            warnings.append(f"WARNING: {name} ({reason}) [owner: {owner}]")
        else:
            reason = "public"
            report.append({"account":acc_name, "checked":len(data), "warnings":[{"name": f"{name}", "reason":f"{reason}", "owner":f"{owner}"}]})
            warnings.append(f"WARNING: {name} ({reason}) [owner: {owner}]")

for b in buckets:
    check_risk(b)

for c in criticals:
    print(c)

for w in warnings:
    print(w)

print()
print(f"Checked {len(buckets)} buckets: {len(criticals)} critical(s), {len(warnings)} warning(s)")

try:
    with open("buckets_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("SUCCESS: Buckets report generated!")
except:
    print("ERROR: Problem writing report to file! Please try again.")
