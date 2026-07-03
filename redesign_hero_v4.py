import io

path = "templates/index.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''<!-- Hero -->
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
    </style>'''

new_block = '''<!-- Hero -->
    <div style="position:relative; max-width:760px; margin:0 auto;">

        <div style="position:absolute; top:-40px; left:50%; transform:translateX(-50%); width:420px; height:320px; background:radial-gradient(ellipse, rgba(233,69,96,0.12), rgba(0,0,0,0) 70%); filter:blur(20px); pointer-events:none; z-index:0;"></div>

        <div style="position:relative; z-index:1; display:flex; align-items:stretch; justify-content:center; gap:20px; flex-wrap:wrap; opacity:0; animation: fadeUp 0.6s ease forwards;">

            <a href="/gm" class="hero-card">
                <div class="hero-card-icon">
                    <span class="hero-emoji">👋</span>
                </div>
                <div class="hero-card-title">GM</div>
                <div class="hero-card-desc">Say good morning onchain, every day</div>
                <div class="hero-card-arrow">→</div>
            </a>

            <a href="/games" class="hero-card hero-card-gold">
                <div class="hero-card-icon hero-card-icon-gold">
                    <span class="hero-emoji hero-emoji-game">🎮</span>
                </div>
                <div class="hero-card-title hero-card-title-gold">Onchain Game</div>
                <div class="hero-card-desc">Play small onchain experiments</div>
                <div class="hero-card-arrow hero-card-arrow-gold">→</div>
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
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .hero-card {
            position:relative;
            width:260px;
            padding:32px 24px 26px;
            border-radius:20px;
            text-decoration:none;
            text-align:left;
            background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
            backdrop-filter: blur(6px);
            border:1px solid rgba(233,69,96,0.22);
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .hero-card:hover {
            transform: translateY(-6px);
            border-color: rgba(233,69,96,0.5);
            box-shadow: 0 16px 34px rgba(233,69,96,0.18);
        }
        .hero-card-gold:hover {
            border-color: rgba(247,179,43,0.5);
            box-shadow: 0 16px 34px rgba(247,179,43,0.18);
        }
        .hero-card-icon {
            width:56px; height:56px; border-radius:16px;
            display:flex; align-items:center; justify-content:center;
            font-size:1.6em;
            background: rgba(233,69,96,0.1);
            border:1px solid rgba(233,69,96,0.25);
            margin-bottom:18px;
        }
        .hero-card-icon-gold {
            background: rgba(247,179,43,0.1);
            border-color: rgba(247,179,43,0.25);
        }
        .hero-emoji {
            display:inline-block;
            animation: wave 1.8s infinite;
        }
        .hero-emoji-game {
            animation: floaty 2.4s ease-in-out infinite;
        }
        .hero-card-title {
            font-family: Georgia, 'Times New Roman', serif;
            font-size:1.5em; font-weight:700;
            color:#fff; margin-bottom:8px;
        }
        .hero-card-title-gold { color:#f7d98a; }
        .hero-card-desc {
            color:rgba(255,255,255,0.45);
            font-size:0.85em; line-height:1.5;
            margin-bottom:22px;
        }
        .hero-card-arrow {
            display:inline-flex; align-items:center; justify-content:center;
            width:34px; height:34px; border-radius:50%;
            color:#e94560;
            border:1px solid rgba(233,69,96,0.3);
            background: rgba(233,69,96,0.06);
            transition: transform 0.3s ease, background 0.3s ease;
        }
        .hero-card-arrow-gold {
            color:#f7b32b;
            border-color: rgba(247,179,43,0.3);
            background: rgba(247,179,43,0.06);
        }
        .hero-card:hover .hero-card-arrow {
            transform: translateX(5px);
            background: rgba(233,69,96,0.16);
        }
        .hero-card:hover .hero-card-arrow-gold {
            background: rgba(247,179,43,0.16);
        }
        @media (max-width: 560px) {
            .hero-card { width:100%; max-width:320px; }
        }
    </style>'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Hero redesigned with glass cards.")
