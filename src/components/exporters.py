import io, zipfile
from typing import List
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait

def save_zip(images: List[Image.Image], prefix="slide"):
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img in enumerate(images, start=1):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            zf.writestr(f"{prefix}_{i:02d}.png", buf.getvalue())
    mem.seek(0)
    return mem.getvalue()

def slides_to_pdf(images: List[Image.Image], dpi=144) -> bytes:
    mem = io.BytesIO()
    w_px, h_px = images[0].size
    w_pt = w_px * 72.0 / dpi
    h_pt = h_px * 72.0 / dpi
    c = canvas.Canvas(mem, pagesize=portrait((w_pt, h_pt)))
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="PNG"); buf.seek(0)
        c.drawImage(buf, 0, 0, width=w_pt, height=h_pt)
        c.showPage()
    c.save(); mem.seek(0)
    return mem.getvalue()

def export_bundle(images: List[Image.Image], project_name="carousel", include_pdf=True) -> bytes:
    """One-click export: PNGs + optional PDF + README in one ZIP."""
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        # PNGs
        for i, img in enumerate(images, start=1):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            zf.writestr(f"{project_name}/png/{project_name}_{i:02d}.png", buf.getvalue())
        # PDF
        if include_pdf:
            pdf = slides_to_pdf(images)
            zf.writestr(f"{project_name}/{project_name}.pdf", pdf)
        # README
        readme = f"""IACubateur Creative Studio Export

Slides: {len(images)}
PDF included: {include_pdf}

Tips:
- LinkedIn Document: upload the PDF.
- Instagram Carousel: upload the PNGs in order.
"""
        zf.writestr(f"{project_name}/README.txt", readme.encode("utf-8"))
    mem.seek(0)
    return mem.getvalue()
