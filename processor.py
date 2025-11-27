from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import os

def modify_image(
    image_path,
    output_folder="modositott_kepek",
    grayscale=True,
    rotate_angle=0,
    resize_dims=None,
    crop_box=None,
    brightness_factor=1.0,
    contrast_factor=1.0,
    sharpen=False,
    text=None,
    text_corner="bal_felso",
    text_size=40,
    text_color=(255, 255, 255)
):
    try:
        with Image.open(image_path) as img:

            if resize_dims:
                img = img.resize(resize_dims)

            if crop_box:
                img = img.crop(crop_box)

            if grayscale:
                img = img.convert("L")

            if rotate_angle != 0:
                img = img.rotate(rotate_angle, expand=True)

            if brightness_factor != 1.0:
                enh = ImageEnhance.Brightness(img)
                img = enh.enhance(brightness_factor)

            if contrast_factor != 1.0:
                enh = ImageEnhance.Contrast(img)
                img = enh.enhance(contrast_factor)

            if sharpen:
                img = img.filter(ImageFilter.SHARPEN)

            if text:
                img = add_text(img, text, text_corner, text_size, text_color)

            os.makedirs(output_folder, exist_ok=True)
            base = os.path.basename(image_path)
            name, ext = os.path.splitext(base)
            out_path = os.path.join(output_folder, f"{name}_modositott{ext}")
            img.save(out_path)
            print(f"Kesz: {out_path}")

    except Exception as e:
        print(f"Hiba: {e}")


def add_text(img, text, corner, size, color):
    img = img.convert("RGB")  # fontos, különben hibát dob
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    iw, ih = img.size
    pad = 10

    if corner == "bal_felso":
        x, y = pad, pad
    elif corner == "jobb_felso":
        x, y = iw - w - pad, pad
    elif corner == "bal_also":
        x, y = pad, ih - h - pad
    else:
        x, y = iw - w - pad, ih - h - pad

    draw.text((x, y), text, fill=color, font=font)
    return img
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    iw, ih = img.size
    pad = 10

    if corner == "bal_felso":
        x, y = pad, pad
    elif corner == "jobb_felso":
        x, y = iw - w - pad, pad
    elif corner == "bal_also":
        x, y = pad, ih - h - pad
    else:
        x, y = iw - w - pad, ih - h - pad

    draw.text((x, y), text, fill=color, font=font)
    return img


def process_folder(folder, config):
    paths = []
    for f in os.listdir(folder):
        ext = f.lower().split(".")[-1]
        if ext in ["jpg", "jpeg", "png", "bmp"]:
            paths.append(os.path.join(folder, f))

    print(f"{len(paths)} kep talalva")
    for p in paths:
        modify_image(p, **config)

def process_multiple_images(paths, config):
    print(f"{len(paths)} kep feldolgozasa indult")
    for p in paths:
        print(f"Kep: {p}")
        modify_image(p, **config)

def process_folder(folder, config):
    paths = []
    for f in os.listdir(folder):
        ext = f.lower().split(".")[-1]
        if ext in ["jpg", "jpeg", "png", "bmp"]:
            paths.append(os.path.join(folder, f))

    print(f"{len(paths)} kep talalva a mappaban")
    for p in paths:
        modify_image(p, **config)
