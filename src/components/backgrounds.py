# components/backgrounds.py
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Couleurs de base
PALETTE = {
    "black": (0, 0, 0),
    "blue": (0, 108, 255),
    "blue_light": (26, 125, 255),
}

def _to_rgba(img):
    return img.convert("RGBA") if img.mode != "RGBA" else img

def neon_grid(w, h):
    img = Image.new("RGB", (w, h), PALETTE["black"])
    d = ImageDraw.Draw(img)
    spacing = int(min(w, h) * 0.08)
    for off in range(-h, w + h, spacing):
        d.line([(off, 0), (off + h, h)], fill=PALETTE["blue"], width=2)
        d.line([(off - 40, 0), (off + h - 40, h)], fill=PALETTE["blue_light"], width=1)
    # vignette douce
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r, a in [(int(w * 0.9), 30), (int(w * 1.2), 80)]:
        od.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], fill=(0, 0, 0, a))
    return _to_rgba(Image.alpha_composite(img.convert("RGBA"), overlay))

def blue_gradient(w, h):
    start = np.array([10, 15, 41], dtype=np.float32)   # #0A0F29
    end   = np.array([0, 108, 255], dtype=np.float32)  # #006CFF
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t = y / max(1, (h - 1))
        col = (start * (1 - t) + end * t).astype(np.uint8)
        arr[y, :, :] = col
    img = Image.fromarray(arr, mode="RGB")
    # bokeh
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for r, a, cx, cy in [
        (int(w * 0.35), 40, int(w * 0.75), int(h * 0.25)),
        (int(w * 0.25), 50, int(w * 0.25), int(h * 0.65)),
    ]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(26, 125, 255, int(a)))
    return _to_rgba(Image.alpha_composite(img.convert("RGBA"), overlay))

def abstract_circles(w, h):
    img = Image.new("RGB", (w, h), PALETTE["black"]).convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for r, a in [
        (int(min(w, h) * 0.55), 28),
        (int(min(w, h) * 0.36), 40),
        (int(min(w, h) * 0.24), 55),
    ]:
        d.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], outline=(0, 108, 255, 120), width=3)
        d.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], fill=(0, 108, 255, int(a / 3)))
    return _to_rgba(Image.alpha_composite(img, overlay))

# --- fonds supplémentaires (optionnels) ---
def diagonal_stripes(w, h):
    img = Image.new("RGB", (w, h), PALETTE["black"])
    d = ImageDraw.Draw(img)
    step = int(min(w, h) * 0.08)
    for i in range(-h, w, step):
        d.rectangle([i, 0, i + step // 2, h], fill=(10, 15, 41))  # bleu nuit
    return _to_rgba(img)

def noise_texture(w, h):
    arr = np.random.randint(0, 30, (h, w), dtype=np.uint8)
    base = np.stack([arr, arr, arr], axis=-1)
    grad = np.linspace(0, 1, h)[:, None]
    blue_layer = (grad * 120).astype(np.uint8)
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[..., 0] = base[..., 0]
    img[..., 1] = base[..., 1]
    img[..., 2] = base[..., 2] + blue_layer
    return _to_rgba(Image.fromarray(img, "RGB").filter(ImageFilter.GaussianBlur(1)))

def radial_glow(w, h):
    img = Image.new("RGB", (w, h), PALETTE["black"])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    max_r = int(max(w, h) * 0.6)
    for r in range(max_r, 0, -40):
        alpha = int(180 * (r / max_r))
        d.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], fill=(0, 108, 255, alpha // 4))
    return _to_rgba(Image.alpha_composite(img.convert("RGBA"), overlay))

def mesh_gradient(w, h):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            t1 = (x / w)
            t2 = (y / h)
            r = int(20 + 60 * t1)
            g = int(20 + 40 * t2)
            b = int(80 + 150 * (1 - t1 * t2))
            arr[y, x] = (r, g, b)
    img = Image.fromarray(arr, "RGB").filter(ImageFilter.GaussianBlur(50))
    return _to_rgba(img)

# Mapping unique et safe
STYLES = {
    "Neon grid": neon_grid,
    "Blue gradient": blue_gradient,
    "Abstract circles": abstract_circles,
    "Diagonal stripes": diagonal_stripes,
    "Noise texture": noise_texture,
    "Radial glow": radial_glow,
    "Mesh gradient": mesh_gradient,
}

def make_background(style: str, w: int, h: int):
    """Toujours retourner une Image RGBA valide, même si le style est inconnu."""
    func = STYLES.get(style)
    if func is None:
        # fallback sûr
        return neon_grid(w, h)
    return func(w, h)
