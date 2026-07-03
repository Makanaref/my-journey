import io

path = "templates/gm.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = """    .lamp-bulb.on {
        border-color: rgba(233,69,96,0.5);
        background: radial-gradient(circle at 50% 38%, #ff7050 0%, #e94560 50%, #6b1020 100%);
    }"""
new1 = """    .lamp-bulb.on {
        border-color: rgba(233,69,96,0.5);
        background: radial-gradient(circle at 50% 38%, #ff7050 0%, #e94560 50%, #6b1020 100%);
        box-shadow: 0 0 10px rgba(233,69,96,0.35);
    }
    .lamp-bulb.flicker {
        animation: lampFlicker 0.7s ease;
    }
    @keyframes lampFlicker {
        0% { filter: brightness(0.3); }
        20% { filter: brightness(1.7); }
        35% { filter: brightness(0.5); }
        55% { filter: brightness(1.4); }
        75% { filter: brightness(0.8); }
        100% { filter: brightness(1); }
    }"""

old2 = """    function updateLamps(count) {
        LAMP_CFG.forEach((_, i) => {
            document.getElementById('bulb-'+i).classList.toggle('on', i < count);
            document.getElementById('glow-'+i).classList.toggle('on', i < count);
        });
        document.getElementById('lamps-count').innerHTML = `<span>${count}</span> GM today`;
    }"""
new2 = """    let lastLampCount = 0;
    function updateLamps(count) {
        LAMP_CFG.forEach((_, i) => {
            const bulb = document.getElementById('bulb-'+i);
            const glow = document.getElementById('glow-'+i);
            const shouldBeOn = i < count;
            const wasOn = i < lastLampCount;
            bulb.classList.toggle('on', shouldBeOn);
            glow.classList.toggle('on', shouldBeOn);
            if (shouldBeOn && !wasOn) {
                bulb.classList.remove('flicker');
                void bulb.offsetWidth;
                bulb.classList.add('flicker');
            }
        });
        document.getElementById('lamps-count').innerHTML = `<span>${count}</span> GM today`;
        lastLampCount = count;
    }"""

errors = []
if old1 not in content: errors.append("part1 (css flicker)")
if old2 not in content: errors.append("part2 (updateLamps function)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Lamp flicker animation added.")
