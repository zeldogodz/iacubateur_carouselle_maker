# filepath: /carouselle-maker/carouselle-maker/src/app.py
import io
import zipfile
from pathlib import Path
from typing import List, Tuple
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from components.backgrounds import make_background
from components.exporters import save_zip, slides_to_pdf

# ====== APP CONFIG ======
st.set_page_config(page_title="IACubateur Creative Studio", page_icon="🧠", layout="wide")

WHS_PRESETS = {
    "Instagram Story / Reel (1080×1920)": (1080, 1920),
    "LinkedIn Carousel Square (1200×1200)": (1200, 1200),
    "LinkedIn Carousel Portrait (1080×1350)": (1080, 1350),
    "Instagram Post Square (1080×1080)": (1080, 1080),
}

PALETTE = {
    "black": "#000000",
    "white": "#FFFFFF",
    "blue":  "#006CFF",
    "blue_light": "#1A7DFF",
    "blue_night": "#0A0F29",
    "grey": "#CCCCCC",
}

DEFAULT_SLIDES = (
    "T’as une idée ?\n\n"
    "Et si l’IA t’aidait à la concrétiser ?\n\n"
    "Un incubateur digital pensé pour les étudiants\n\n"
    "Rejoins-nous sur iacubateur.com"
)

# ===== utilities =====
def load_font_file(file, fallback_size=64):
    if file is None:
        return ImageFont.load_default()
    data = file.read()
    return ImageFont.truetype(io.BytesIO(data), size=fallback_size)

def wrap_text(draw, text, font, max_w):
    lines = []
    for raw in text.split("\n"):
        if not raw.strip():
            lines.append("")
            continue
        cur, buf = "", []
        for w in raw.split(" "):
            test = (cur + (" " if cur else "") + w).strip()
            if draw.textlength(test, font=font) <= max_w or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def auto_font_size(draw, text, base_size, w, h, margin, min_size=28):
    size = base_size
    while size >= min_size:
        font = ImageFont.truetype(font.path, size=size) if hasattr(font, "path") else None
        if font is None:
            font = ImageFont.load_default()
            return font, size
        lines = wrap_text(draw, text, font, w - 2*margin)
        total_h = sum(font.getbbox(t)[3] for t in lines) + (len(lines)-1)*int(size*0.25)
        if total_h <= h - 2*margin:
            return font, size
        size -= 2
    return ImageFont.truetype(font.path, size=min_size), min_size

def draw_slide(
    canvas_w, canvas_h, bg_style, text, title_font, body_font,
    highlight_words: Tuple[str,...], logo_rgba: Image.Image|None, logo_width_pct=0.32,
    top_title_mode=False
):
    img = make_background(bg_style, canvas_w, canvas_h)
    # Vérification du type et du mode de l'image
    if not isinstance(img, Image.Image):
        raise TypeError("make_background doit retourner une image PIL.Image.Image")
    if img.mode not in ("RGBA", "RGB"):
        img = img.convert("RGBA")

    draw = ImageDraw.Draw(img)
    MARGIN = int(min(canvas_w, canvas_h) * 0.08)

    chosen_font = title_font if (len(text) <= 40 and "\n" not in text) else body_font

    max_w = canvas_w - 2*MARGIN
    lines = wrap_text(draw, text.strip(), chosen_font, max_w)
    line_gap = int(chosen_font.size * 0.25)
    total_h = sum(chosen_font.getbbox(t)[3] for t in lines) + (len(lines)-1)*line_gap

    if top_title_mode:
        y = MARGIN
    else:
        y = (canvas_h - total_h)//2

    for line in lines:
        lw = draw.textlength(line, font=chosen_font)
        x = (canvas_w - lw)//2
        cur_x = x
        for token in (line.split(" ") if line else [""]):
            tok_disp = (token + " ") if token else " "
            base = PALETTE["white"]
            if any(token.lower().strip(",.!?") == k.lower() for k in highlight_words):
                base = PALETTE["blue"]
            draw.text((cur_x, y), tok_disp, font=chosen_font, fill=base)
            cur_x += draw.textlength(tok_disp, font=chosen_font)
        y += chosen_font.getbbox(line)[3] + line_gap

    if logo_rgba:
        lw = int(canvas_w * logo_width_pct)
        w0, h0 = logo_rgba.size
        r = lw / w0
        logo = logo_rgba.resize((int(w0*r), int(h0*r)), Image.LANCZOS)
        lx = (canvas_w - logo.width)//2
        ly = canvas_h - logo.height - MARGIN
        img.alpha_composite(logo, (lx, ly))

    return img

# ====== UI ======
st.title("🧩 IACubateur Creative Studio")
st.caption("Génère des carrousels Stories/Reels, carrousels LinkedIn, et posts texte.")

tabs = st.tabs(["🎞️ Visual Builder", "📝 Text Post Generator", "⚙️ About"])

with tabs[0]:
    colA, colB = st.columns([1.2, 1])
    with colA:
        preset_name = st.selectbox("Format", list(WHS_PRESETS.keys()))
        W, H = WHS_PRESETS[preset_name]
        bg_style = st.selectbox("Background style", [
            "Neon grid", "Blue gradient", "Abstract circles",
            "Diagonal stripes", "Noise texture", "Radial glow", "Mesh gradient"
        ])
        slide_texts = st.text_area(
            "Slides (un paragraphe = un slide)",
            height=220,
            value=DEFAULT_SLIDES
        )
        highlight_input = st.text_input("Mots à mettre en bleu (séparés par des virgules)", value="IA,iacubateur.com,étudiants,incubateur")
        highlight_words = tuple([w.strip() for w in highlight_input.split(",") if w.strip()])

        st.subheader("Typographies")
        t1, t2 = st.columns(2)
        with t1:
            font_title_file = st.file_uploader("Police TITRES (ex: Montserrat-Bold.ttf)", type=["ttf","otf"])
            title_size = st.slider("Taille titres", 48, 140, 92, 2)
        with t2:
            font_body_file = st.file_uploader("Police TEXTE (ex: Inter-Regular.ttf)", type=["ttf","otf"])
            body_size = st.slider("Taille texte", 40, 100, 60, 2)

        st.subheader("Branding")
        logo_file = st.file_uploader("Logo PNG (fond transparent)", type=["png"])
        logo_width_pct = st.slider("Largeur logo (pourcentage de la largeur)", 0.15, 0.6, 0.32, 0.01)

        run = st.button("🚀 Générer")
    with colB:
        st.markdown("**Exports**")
        want_zip = st.checkbox("ZIP (PNG)", value=True)
        want_pdf = st.checkbox("PDF carrousel (LinkedIn)", value=("LinkedIn" in preset_name))
        st.info("Astuce : pour LinkedIn, le format Document PDF multi-pages marche très bien.")

    if run:
        def load_truetype(file, size, fallback="default"):
            if file is None:
                return ImageFont.load_default() if fallback == "default" else ImageFont.truetype(fallback, size=size)
            file.seek(0)
            data = file.read()
            return ImageFont.truetype(io.BytesIO(data), size=size)

        title_font = load_truetype(font_title_file, title_size)
        body_font  = load_truetype(font_body_file,  body_size)

        logo_rgba = None
        if logo_file:
            logo_rgba = Image.open(logo_file).convert("RGBA")

        slides = [s.strip() for s in slide_texts.split("\n\n") if s.strip()]
        outputs: List[Image.Image] = []
        for idx, text in enumerate(slides, start=1):
            img = draw_slide(
                W, H, bg_style, text, title_font, body_font,
                highlight_words, logo_rgba, logo_width_pct, top_title_mode=False
            )
            outputs.append(img)

        st.success(f"{len(outputs)} slides générés ✅")
        for i, im in enumerate(outputs, 1):
            st.image(im, caption=f"Slide {i}", use_container_width=True)

        if want_zip:
            zip_bytes = save_zip(outputs, prefix="slide")
            st.download_button("⬇️ Télécharger ZIP (PNG)", data=zip_bytes, file_name="carousel.zip", mime="application/zip")
        if want_pdf:
            pdf_bytes = slides_to_pdf(outputs, dpi=144)
            st.download_button("⬇️ Télécharger PDF (LinkedIn)", data=pdf_bytes, file_name="carousel.pdf", mime="application/pdf")

with tabs[1]:
    st.subheader("Générateur de posts texte")
    platform = st.selectbox("Plateforme", ["LinkedIn", "Instagram"])
    tone = st.selectbox("Ton", ["Pro", "Étudiant (friendly)", "Punchy court"])
    goal = st.text_input("Objectif (ex : recruter des bêta-testeurs, annoncer l’ouverture…)", value="Rejoindre IACubateur et déposer un projet")
    bullets = st.text_area("Points clés (un par ligne)", value="Experts IA 24/7\nCommunauté d’étudiants\nProgramme personnalisé\nDiagnostic gratuit")
    url = st.text_input("Lien d’appel à l’action", value="https://iacubateur.com")

    if st.button("✍️ Générer le texte"):
        pts = [b.strip(" -•\t") for b in bullets.splitlines() if b.strip()]
        if tone == "Pro":
            opener = "Incube ton projet, plus vite et mieux."
        elif tone == "Étudiant (friendly)":
            opener = "Tu as une idée ? On t’aide à la transformer en projet."
        else:
            opener = "Passe à l’action. Lance ton projet."

        lines = [opener, ""]
        lines += [f"• {p}" for p in pts]
        lines += ["", f"👉 En savoir plus : {url}"]
        post_text = "\n".join(lines)
        st.code(post_text, language=None)
        st.download_button("⬇️ Télécharger .txt", data=post_text.encode("utf-8"), file_name=f"post_{platform.lower()}.txt", mime="text/plain")

with tabs[2]:
    st.markdown("""
**IACubateur Creative Studio**  
– Stories/Reels, carrousels LinkedIn (PNG+PDF), posts texte  
– Arrière-plans : néon, gradient, cercles abstraits  
– Highlights automatiques (mots en bleu)  
""")