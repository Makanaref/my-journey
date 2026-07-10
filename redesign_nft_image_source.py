import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace CSS for radio-row with toggle-style buttons
old_css = '''    .radio-row { display: flex; gap: 14px; margin-bottom: 14px; }
    .radio-option { display: flex; align-items: center; gap: 6px; font-size: 0.85em; color: #ccc; cursor: pointer; }'''
new_css = '''    .toggle-row { display: flex; gap: 8px; margin-bottom: 14px; }
    .toggle-option {
        flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px;
        padding: 11px 10px; border-radius: 10px; font-size: 0.82em; color: #999;
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);
        cursor: pointer; transition: all 0.2s ease;
    }
    .toggle-option input { display: none; }
    .toggle-option.active {
        color: #0f1420; background: #7ec8e3; border-color: #7ec8e3; font-weight: 700;
    }
    .toggle-option:hover:not(.active) { border-color: rgba(126,200,227,0.4); color: #ccc; }
    .upload-zone {
        border: 1.5px dashed rgba(126,200,227,0.3); border-radius: 12px;
        padding: 24px 16px; text-align: center; cursor: pointer;
        transition: border-color 0.2s ease, background 0.2s ease; position: relative;
    }
    .upload-zone:hover { border-color: rgba(126,200,227,0.6); background: rgba(126,200,227,0.03); }
    .upload-zone input[type="file"] {
        position: absolute; inset: 0; opacity: 0; cursor: pointer;
    }
    .upload-zone-text { color: #7ec8e3; font-size: 0.85em; font-weight: 600; margin-top: 8px; }
    .upload-zone-sub { color: rgba(255,255,255,0.35); font-size: 0.72em; margin-top: 4px; }'''

# 2. Replace image source HTML block
old_img = '''            <div class="radio-row">
                <label class="radio-option"><input type="radio" name="img-source" value="url" checked onchange="toggleImageSource('url')"> Paste URL</label>
                <label class="radio-option"><input type="radio" name="img-source" value="upload" onchange="toggleImageSource('upload')"> Upload file</label>
            </div>
            <input type="text" id="nft-image-url" placeholder="https://...">
            <input type="file" id="nft-image-file" accept="image/png,image/jpeg,image/gif,image/webp" style="display:none;">
            <img id="nft-image-preview" class="image-preview">'''
new_img = '''            <div class="toggle-row">
                <label class="toggle-option active" id="opt-url" onclick="toggleImageSource('url')">
                    <input type="radio" name="img-source" value="url" checked> 🔗 Paste URL
                </label>
                <label class="toggle-option" id="opt-upload" onclick="toggleImageSource('upload')">
                    <input type="radio" name="img-source" value="upload"> 📁 Upload file
                </label>
            </div>
            <input type="text" id="nft-image-url" placeholder="https://...">
            <label class="upload-zone" id="upload-zone" style="display:none;">
                <input type="file" id="nft-image-file" accept="image/png,image/jpeg,image/gif,image/webp">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" style="margin:0 auto; display:block;">
                    <path d="M12 16V4M12 4l-4 4M12 4l4 4" stroke="#7ec8e3" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2" stroke="#7ec8e3" stroke-width="1.6" stroke-linecap="round"/>
                </svg>
                <div class="upload-zone-text" id="upload-zone-label">Click to choose an image</div>
                <div class="upload-zone-sub">PNG, JPG, GIF or WEBP</div>
            </label>
            <img id="nft-image-preview" class="image-preview">'''

# 3. Replace mint price radio block
old_price = '''            <div class="radio-row">
                <label class="radio-option"><input type="radio" name="price-type" value="free" checked onchange="togglePriceType('free')"> Free (network fee only)</label>
                <label class="radio-option"><input type="radio" name="price-type" value="paid" onchange="togglePriceType('paid')"> Set a price</label>
            </div>'''
new_price = '''            <div class="toggle-row">
                <label class="toggle-option active" id="opt-free" onclick="togglePriceType('free')">
                    <input type="radio" name="price-type" value="free" checked> 🎁 Free
                </label>
                <label class="toggle-option" id="opt-paid" onclick="togglePriceType('paid')">
                    <input type="radio" name="price-type" value="paid"> 💰 Set a price
                </label>
            </div>'''

errors = []
if old_css not in content: errors.append("css")
if old_img not in content: errors.append("image html")
if old_price not in content: errors.append("price html")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old_css, new_css, 1)
    content = content.replace(old_img, new_img, 1)
    content = content.replace(old_price, new_price, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Image source and price UI redesigned.")
