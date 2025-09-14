def save_zip(images, prefix="slide"):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, img in enumerate(images):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            zip_file.writestr(f"{prefix}_{idx + 1}.png", img_byte_arr.getvalue())
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def slides_to_pdf(images, dpi=144):
    pdf_buffer = io.BytesIO()
    first_image = images[0]
    first_image.save(pdf_buffer, format='PDF', save_all=True, append_images=images[1:], resolution=dpi)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()