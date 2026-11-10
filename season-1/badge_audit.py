badges = [
    {"owner": "Dave", "active": True, "last_used_days": 1},
    {"owner": "intern-temp", "active": True, "last_used_days": 140},
    {"active": True, "last_used_days": 3},
    {"last_used_days": 5},
    {"owner": "Gary", "active": False},
    {"owner": "Tomasz", "last_used_days": 200},
]

findings = []

oks = []
criticals = []
warnings = []

def check_badge(badge):
    owner = badge.get('owner', "UNKNOWN")
    active = badge.get('active', True)
    note = ", active status missing, so assumed active"

    if "active" not in badge and "owner" not in badge:
        return {"owner": owner, "verdict": "CRITICAL", "reason": f"without owner{note}"}
    elif not active:
        return {"owner": owner, "verdict": "OK", "reason": "badge deactivated"}
    elif "owner" not in badge:
        if "active" not in badge:
            return {"owner": owner, "verdict": "CRITICAL", "reason": f"active badge without owner{note}"}
        else:
            return {"owner": owner, "verdict": "CRITICAL", "reason": "active badge without owner"}
    elif "last_used_days" not in badge:
        if "active" not in badge:
            return {"owner": owner, "verdict": "WARNING", "reason": f"no last-used date, assumed WARNING{note}"}
        else:
            return {"owner": owner, "verdict": "WARNING", "reason": "no last-used date, assumed WARNING"}
    elif badge['last_used_days'] > 90:
        if "active" not in badge:
            return {"owner": owner, "verdict": "WARNING", "reason": f"unused for {badge['last_used_days']} days{note}"}        
        else:
            return {"owner": owner, "verdict": "WARNING", "reason": f"unused for {badge['last_used_days']} days"}        
    else:
        if "active" not in badge:
            return {"owner": owner, "verdict": "OK", "reason": f"last used {badge['last_used_days']} day(s) ago{note}"}
        else:
            return {"owner": owner, "verdict": "OK", "reason": f"last used {badge['last_used_days']} day(s) ago"}
        
for b in badges:
    finding = check_badge(b)
    findings.append(finding)

for f in findings:
    finding = f"{f['verdict']}: {f['owner']} ({f['reason']})"
    print(finding)
    
    if f['verdict'] == "OK":
        oks.append(finding)
    elif f['verdict'] == "CRITICAL":
        criticals.append(finding)
    elif f['verdict'] == "WARNING":
        warnings.append(finding)
   
print()
print(f"Checked {len(findings)} badges: {len(criticals)} critical(s), {len(warnings)} warning(s), {len(oks)} ok")
