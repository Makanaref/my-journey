import os
import shutil
from app import app

OUTPUT_DIR = "static_build"

ROUTES = {
    "/": "index.html",
    "/about": "about.html",
    "/contact": "contact.html",
    "/weather": "weather.html",
    "/currency": "currency.html",
    "/calculator": "calculator.html",
    "/notes": "notes.html",
    "/converter": "converter.html",
    "/reminder": "reminder.html",
    "/dashboard": "dashboard.html",
    "/tools": "tools.html",
    "/oracle": "oracle.html",
    "/games": "games.html",
    "/mint": "mint.html",
    "/domain": "domain.html",
    "/deploy-contract": "deploy_contract.html",
    "/flip": "flip.html",
    "/mint-nft": "mint-nft.html",
    "/marketplace": "marketplace.html",
    "/my-nfts": "my-nfts.html",
    "/my-store": "my-store.html",
    "/gm": "gm.html",
    "/b20": "b20.html",
    "/swap": "swap.html",
    "/networks": "networks.html",
    "/privacy": "privacy.html",
    "/terms": "terms.html",
    "/todo": "todo.html",
    "/timer": "timer.html",
    "/stopwatch": "stopwatch.html",
    "/wordcount": "wordcount.html",
    "/speedtest": "speedtest.html",
    "/password": "password.html",
    "/color": "color.html",
    "/tip": "tip.html",
    "/bmi": "bmi.html",
    "/age": "age.html",
    "/dice": "dice.html",
    "/guess": "guess.html",
    "/random": "random.html",
    "/quote": "quote.html",
    "/counter": "counter.html",
    "/blog": "blog.html",
    "/skills": "skills.html",
    "/timeline": "timeline.html",
    "/faq": "faq.html",
    "/coin": "coin.html",
}

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

client = app.test_client()
failed = []

for route, filename in ROUTES.items():
    try:
        resp = client.get(route)
        if resp.status_code != 200:
            failed.append((route, resp.status_code))
            continue
        out_path = os.path.join(OUTPUT_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(resp.data)
        if filename == "index.html":
            pass
    except Exception as e:
        failed.append((route, str(e)))

shutil.copytree("static", os.path.join(OUTPUT_DIR, "static"))

print("Done.")
print("Generated:", len(ROUTES) - len(failed), "pages")
if failed:
    print("Failed:")
    for r in failed:
        print(" ", r)
