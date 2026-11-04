rules = [
    {"name": "web-https",             "port": 443,  "source": "0.0.0.0/0"},
    {"name": "garys-caravan-rdp",     "port": 3389, "source": "0.0.0.0/0"},
    {"name": "admin-ssh",             "port": 22,   "source": "10.0.0.0/16"},
    {"name": "tomasz-postgres-debug", "port": 5432, "source": "0.0.0.0/0"},
    {"name": "brian-legacy-ssh",      "port": 22},
    {"name": "web-http",              "port": 80,   "source": "0.0.0.0/0"},
]

criticals = []
warnings = []

def is_risky(port):
    if port == 3389 or port == 22:
        return True
    return False

def rule_verdict(rule):
    port = rule['port']
    name = rule['name']
    source = rule.get('source', '0.0.0.0/0')
    
    if source == "0.0.0.0/0" and is_risky(port):
        criticals.append(name)
        return "CRITICAL" 
    elif source == "0.0.0.0/0" and (port == 80 or port == 443):
        return "OK"
    elif source == "0.0.0.0/0" and not is_risky(port):
        warnings.append(name)
        return "WARNING"
    else:
        return "OK"

for r in rules:
    rule_verdict(r)        

for c in criticals:
    print("CRITICAL:", c)

for w in warnings:
    print("WARNING:", w)

print()
print("Checked", len(rules), "rules:", len(criticals), "critical(s).", len(warnings), "warning(s)")
