# NoctuLabs

Hands-on cloud security labs: Python auditing scripts now, with Azure, Terraform and CI/CD security to come. This is a public learning log: every script here was rebuilt from a blank file to prove I can write it without notes.

Each lab is set at **NoctuNest**, a fictional fintech with a sitcom-worthy cast and a habit of misconfiguring its cloud. NoctuNest is entirely fictional, and all data in this repo is dummy data.

## Season 1: Auditing NoctuNest's cloud

### `auditor_rebuild.py`: storage bucket auditor
Loads a JSON export of storage buckets and classifies each one:

| Verdict | Rule |
|---|---|
| CRITICAL | Public **and** unencrypted |
| WARNING | Public **or** unencrypted |
| OK | Private and encrypted |

**Fail-safe defaults:** if a bucket is missing its `public` or `encrypted` field, the auditor assumes the worst case (public, unencrypted) rather than letting it pass silently. Unknown means risky until proven otherwise.

Output lists critical findings first, then warnings, then a summary count.

### `firewall.py`: inbound rule auditor
Checks inbound firewall rules (like AWS security groups or Azure NSG rules) and flags any rule open to the internet (`0.0.0.0/0`).

| Verdict | Rule |
|---|---|
| CRITICAL | Open to the internet on an admin port: 22 (SSH) or 3389 (RDP) |
| WARNING | Open to the internet on any port other than 80 (HTTP) or 443 (HTTPS) |
| OK | Everything else |

**Fail-safe defaults:** a rule with no `source` is treated as `0.0.0.0/0` (any IPv4 address), so an incomplete rule is flagged rather than silently passed.

## How to run
Requires Python 3. No external packages.

```bash
cd season-1
python3 auditor_rebuild.py
python3 firewall.py
```

## What's next
- Season 2: Azure core (VNets, NSGs, storage, RBAC, Key Vault): build it, break it, fix it
- Season 3: Terraform on Azure
- Season 4: CI/CD with security scanning
