import io

path = "templates/index.html"

old_block = """<!-- Hero -->
    <div style="position:relative; max-width:640px; margin:0 auto;">

        <div style="position:absolute; top:-30px; left:50%; transform:translateX(-50%); width:300px; height:300px; background:radial-gradient(circle, rgba(233,69,96,0.14), rgba(0,0,0,0) 70%); filter:blur(10px); pointer-events:none; z-index:0;"></div>

        <div style="position:relative; z-index:1;">

            <div style="opacity:0; animation: fadeUp 0.6s ease forwards;">
                <div style="position:relative; width:84px; height:84px; margin:0 auto 24px;">
                    <div style="position:absolute; inset:-5px; border-radius:50%; background:conic-gradient(from 0deg, #e94560, #f7b32b, #e94560); animation: spin 6s linear infinite; opacity:0.6;"></div>
                    <div style="position:absolute; inset:3px; border-radius:50%; background:#161c2e; display:flex; align-items:center; justify-content:center; font-size:1.9em;">
                        <a href="/gm" style="text-decoration:none; display:inline-block; animation: wave 1.6s infinite;">👋</a>
                    </div>
                </div>
            </div>

            <div style="display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:36px; opacity:0; animation: fadeUp 0.6s ease 0.1s forwards;">
                <span style="display:inline-flex; align-items:center; gap:8px; padding:6px 16px; border-radius:999px; border:1px solid rgba(46,204,113,0.35); background:rgba(46,204,113,0.08); font-size:0.85em; color:#2ecc71;">
                    <span style="width:8px; height:8px; border-radius:50%; background:#2ecc71; box-shadow:0 0 8px #2ecc71; animation: blinkDot 1.8s infinite;"></span>
                    Available for work
                </span>
                <a href="/gm" class="gm-pill" style="display:inline-flex; align-items:center; gap:6px; padding:6px 16px; border-radius:999px; border:1px solid rgba(233,69,96,0.35); background:rgba(233,69,96,0.08); font-size:0.85em; color:#e94560; text-decoration:none;">
                    Say GM
                </a>
            </div>

        </div>
    </div>

    <style>
        @keyframes wave {
            0%, 60%, 100% { transform: rotate(0deg); }
            10% { transform: rotate(14deg); }
            20% { transform: rotate(-8deg); }
            30% { transform: rotate(14deg); }
            40% { transform: rotate(-4deg); }
            50% { transform: rotate(10deg); }
        }
        @keyframes blinkDot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.35; }
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .hero-cta-primary {
            display:inline-flex; align-items:center; gap:8px;
            padding:13px 28px; border-radius:12px; font-weight:700; font-size:1em;
            text-decoration:none; color:#fff;
            background:linear-gradient(135deg, #e94560, #f7253a);
            box-shadow:0 8px 20px rgba(233,69,96,0.3);
            transition:transform 0.25s ease, box-shadow 0.25s ease;
        }
        .hero-cta-primary:hover {
            transform:translateY(-3px);
            box-shadow:0 12px 28px rgba(233,69,96,0.45);
        }
        .hero-cta-primary:hover span { transform:translateX(4px); }
        .hero-cta-outline {
            display:inline-flex; align-items:center;
            padding:13px 28px; border-radius:12px; font-weight:600; font-size:1em;
            text-decoration:none; color:#fff;
            border:1px solid rgba(255,255,255,0.18);
            background:rgba(255,255,255,0.03);
            transition:transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
        }
        .hero-cta-outline:hover {
            transform:translateY(-3px);
            background:rgba(255,255,255,0.07);
            border-color:rgba(255,255,255,0.3);
        }
        .gm-pill {
            transition:transform 0.2s ease, background 0.2s ease;
        }
        .gm-pill:hover {
            transform:translateY(-2px);
            background:rgba(233,69,96,0.16);
        }
    </style>"""

new_block = """<!-- Hero -->
    <div style="position:relative; max-width:640px; margin:0 auto;">

        <div style="position:absolute; top:-30px; left:50%; transform:translateX(-50%); width:340px; height:340px; background:radial-gradient(circle, rgba(233,69,96,0.14), rgba(0,0,0,0) 70%); filter:blur(14px); pointer-events:none; z-index:0;"></div>

        <div style="position:relative; z-index:1; display:flex; align-items:flex-start; justify-content:center; gap:56px; flex-wrap:wrap; transform:translateX(-18px); opacity:0; animation: fadeUp 0.6s ease forwards;">

            <a href="/gm" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:14px;">
                <div class="orb">
                    <div class="orb-glow"></div>
                    <div class="orb-ring"></div>
                    <div class="orb-core">
                        <span class="orb-emoji">👋</span>
                    </div>
                </div>
                <span class="orb-label" style="background:linear-gradient(90deg, #ffffff, #e94560 70%); -webkit-background-clip:text; background-clip:text; color:transparent;">GM</span>
            </a>

            <a href="/games" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:14px;">
                <div class="orb">
                    <div class="orb-glow orb-glow-gold"></div>
                    <div class="orb-ring orb-ring-gold"></div>
                    <div class="orb-core">
                        <span class="orb-emoji orb-emoji-game">🎮</span>
                    </div>
                </div>
                <span class="orb-label" style="color:#f7b32b;">Onchain Game</span>
            </a>

        </div>
    </div>

    <style>
        @keyframes wave {
            0%, 60%, 100% { transform: rotate(0deg); }
            10% { transform: rotate(14deg); }
            20% { transform: rotate(-8deg); }
            30% { transform: rotate(14deg); }
            40% { transform: rotate(-4deg); }
            50% { transform: rotate(10deg); }
        }
        @keyframes floaty {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px) translateX(-18px); }
            to { opacity: 1; transform: translateY(0) translateX(-18px); }
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @keyframes pulseGlow {
            0%, 100% { opacity: 0.55; transform: scale(1); }
            50% { opacity: 0.9; transform: scale(1.12); }
        }
        .orb {
            position:relative; width:100px; height:100px;
            animation: floaty 3.4s ease-in-out infinite;
        }
        .orb-glow {
            position:absolute; inset:-14px; border-radius:50%;
            background: radial-gradient(circle, rgba(233,69,96,0.55), rgba(233,69,96,0) 70%);
            animation: pulseGlow 2.6s ease-in-out infinite;
            z-index:0;
        }
        .orb-glow-gold {
            background: radial-gradient(circle, rgba(247,179,43,0.55), rgba(247,179,43,0) 70%);
        }
        .orb-ring {
            position:absolute; inset:-4px; border-radius:50%;
            background:conic-gradient(from 0deg, #e94560, #7b2ff7, #e94560);
            animation: spin 5s linear infinite;
            z-index:1;
        }
        .orb-ring-gold {
            background:conic-gradient(from 0deg, #f7b32b, #e94560, #f7b32b);
        }
        .orb-core {
            position:absolute; inset:4px; border-radius:50%;
            background: radial-gradient(circle at 32% 28%, #232a47, #0a0d1a 78%);
            display:flex; align-items:center; justify-content:center;
            font-size:2.15em;
            box-shadow: inset 0 0 18px rgba(0,0,0,0.65), 0 0 26px rgba(233,69,96,0.3);
            z-index:2;
        }
        .orb-emoji {
            display:inline-block;
            animation: wave 1.8s infinite;
            filter: drop-shadow(0 0 8px rgba(255,255,255,0.35));
        }
        .orb-emoji-game {
            animation: floaty 2.2s ease-in-out infinite;
            filter: drop-shadow(0 0 8px rgba(247,179,43,0.45));
        }
        .orb-label {
            font-family: Georgia, 'Times New Roman', serif;
            font-size:1.3em;
            font-weight:700;
            letter-spacing:0.04em;
        }
    </style>"""

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_block not in content:
    print("ERROR hero: old_block not found!")
else:
    content = content.replace(old_block, new_block)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Hero orbs applied.")
