with open("templates/admin.html", "r", encoding="utf-8") as f:
    admin_content = f.read()

old_read_form = '<form method="POST" action="/admin/read/{{ m.id }}">'
new_read_form = '<form method="POST" action="/admin/read/{{ m.id }}">\n                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">'
if old_read_form not in admin_content:
    raise SystemExit("ERROR: read form not found in admin.html")
admin_content = admin_content.replace(old_read_form, new_read_form, 1)

old_delete_form = '<form method="POST" action="/admin/delete/{{ m.id }}" onsubmit="return confirm(\'Delete this message?\');">'
new_delete_form = '<form method="POST" action="/admin/delete/{{ m.id }}" onsubmit="return confirm(\'Delete this message?\');">\n                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">'
if old_delete_form not in admin_content:
    raise SystemExit("ERROR: delete form not found in admin.html")
admin_content = admin_content.replace(old_delete_form, new_delete_form, 1)

with open("templates/admin.html", "w", encoding="utf-8") as f:
    f.write(admin_content)

with open("templates/admin_login.html", "r", encoding="utf-8") as f:
    login_content = f.read()

old_login_form = '<form method="POST">'
new_login_form = '<form method="POST">\n        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">'
if old_login_form not in login_content:
    raise SystemExit("ERROR: login form not found in admin_login.html")
login_content = login_content.replace(old_login_form, new_login_form, 1)

with open("templates/admin_login.html", "w", encoding="utf-8") as f:
    f.write(login_content)

print("Done. CSRF tokens added to admin.html and admin_login.html.")
