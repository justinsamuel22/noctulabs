servers = [
    {"name": "pay-api", "public": True, "last_patched_days": 120},
    {"name": "hr-db", "public": False, "last_patched_days": 200},
    {"name": "web-front", "public": True, "last_patched_days": 12},
    {"name": "build-agent", "public": False, "last_patched_days": 90},
    {"name": "old-ftp", "last_patched_days": 400},
    {"name": "badge-reader", "public": True},
    {"name": "mystery-box"},
]

criticals = 0
warnings = 0
ok = 0

def patch_text(server):
    lpd = server.get('last_patched_days')

    if "last_patched_days" in server:
        return f"last patched {lpd} days ago"
    else:
        return "patch date UNKNOWN (assumed overdue)"
 
def public_text(server):
    p = server.get('public', True)
    
    if "public" in server:
        if p:
            return "public"
        else:
            return "private"
    else:
        return "public status UNKNOWN (assumed public)"

def check_risk(server):
    public = public_text(server)
    patched = patch_text(server)
    
    if "UNKNOWN" in patched and "UNKNOWN" in public:
        return "CRITICAL"
    elif "last_patched_days" in server:
        lpd = 'last_patched_days'
        if "public" in public and server[lpd] > 90:
            return "CRITICAL"
        elif "private" in public and server[lpd] > 90:
            return "WARNING"
        else:
            return "OK"
    elif "public" in public:
        return "CRITICAL"
    elif "private" in public:
        return "WARNING"
    else:
        return "OK"

for s in servers:
    risk_output = f"{check_risk(s)} {s.get('name')}: {public_text(s)}, {patch_text(s)}"
    if "CRITICAL" in risk_output:
        criticals += 1    
    elif "WARNING" in risk_output:
        warnings += 1
    elif "OK" in risk_output:
        ok += 1   
    print(risk_output)

total_servers = criticals + warnings + ok

print(f"Summary: {total_servers} servers checked, {criticals} CRITICAL, {warnings} WARNING, {ok} OK")
