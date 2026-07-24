import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSRFProtect import after flask_limiter imports
old_imports = "from flask_limiter.util import get_remote_address"
new_imports = "from flask_limiter.util import get_remote_address\nfrom flask_wtf import CSRFProtect"
if old_imports not in content:
    raise SystemExit("ERROR: flask_limiter import line not found, aborting.")
content = content.replace(old_imports, new_imports, 1)

# 2. Initialize CSRFProtect after Talisman setup, before Limiter
old_talisman = "Talisman(app, content_security_policy=csp, force_https=False)"
new_talisman = "Talisman(app, content_security_policy=csp, force_https=False)\n\n# CSRF Protection\ncsrf = CSRFProtect(app)"
if old_talisman not in content:
    raise SystemExit("ERROR: Talisman init line not found, aborting.")
content = content.replace(old_talisman, new_talisman, 1)

# 3. Exempt JSON/fetch-based API routes from CSRF (they don't send csrf_token form field)
exempt_routes = [
    '@app.route("/api/contact", methods=["POST"])\n@limiter.limit("10 per hour")',
    '@app.route("/api/shorten", methods=["POST"])\n@limiter.limit("30 per hour")',
    '@app.route("/api/nft/upload-image", methods=["POST"])\n@limiter.limit("20 per hour")',
    '@app.route("/api/nft/create-metadata", methods=["POST"])\n@limiter.limit("20 per hour")',
]

for old_block in exempt_routes:
    if old_block not in content:
        raise SystemExit(f"ERROR: route block not found, aborting:\n{old_block}")
    route_line, limiter_line = old_block.split("\n")
    new_block = f"{route_line}\n@csrf.exempt\n{limiter_line}"
    content = content.replace(old_block, new_block, 1)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. app.py updated with CSRF protection and exemptions.")
