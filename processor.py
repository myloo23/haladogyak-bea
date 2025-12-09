from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import os

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def normalize_crop_box(img, crop_box):
    """
    Elfogadja:
    - (bal, felso, jobb, also)  -> klasszikus PIL
    - (bal, felso, szelesseg, magassag) -> autodetekt, ha jobb<=bal vagy also<=felso
    """
    l, t, a, b = map(int, crop_box)

    # Autodetekt: ha a 'jobb/also' nem lehet érvényes koordináta,
    # akkor tekintsük szélesség/magasságnak
    if a <= l or b <= t:
        r = l + a
        bottom = t + b
    else:
        r, bottom = a, b

    iw, ih = img.size

    # Clamp bounds
    l = max(0, min(l, iw))
    t = max(0, min(t, ih))
    r = max(0, min(r, iw))
    bottom = max(0, min(bottom, ih))

    if r <= l or bottom <= t:
        raise ValueError(f"Ervenytelen crop_box: {crop_box} -> {(l, t, r, bottom)}")

    return (l, t, r, bottom)


def anchor_crop_box(img, corner, width, height):
    """
    Sarokhoz rögzített kivágás:
    corner: bal_felso, jobb_felso, bal_also, jobb_also
    width/height: kivágás mérete
    """
    iw, ih = img.size
    width = max(1, min(int(width), iw))
    height = max(1, min(int(height), ih))

    if corner == "bal_felso":
        l, t = 0, 0
    elif corner == "jobb_felso":
        l, t = iw - width, 0
    elif corner == "bal_also":
        l, t = 0, ih - height
    else:  # jobb_also
        l, t = iw - width, ih - height

    return (l, t, l + width, t + height)


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

            # Resize
            if resize_dims:
                w, h = map(int, resize_dims)
                img = img.resize((w, h), resample=Image.LANCZOS)

            # Crop
            if crop_box:
                # "sarok + meret" mód dictként
                if isinstance(crop_box, dict) and crop_box.get("mode") == "anchor":
                    box = anchor_crop_box(
                        img,
                        crop_box.get("corner", "bal_felso"),
                        crop_box["width"],
                        crop_box["height"]
                    )
                    img = img.crop(box)
                else:
                    box = normalize_crop_box(img, crop_box)
                    img = img.crop(box)

            # Grayscale
            if grayscale:
                img = img.convert("L")

            # Rotate
            if rotate_angle != 0:
                img = img.rotate(rotate_angle, expand=True)

            # Brightness
            if brightness_factor != 1.0:
                enh = ImageEnhance.Brightness(img)
                img = enh.enhance(brightness_factor)

            # Contrast
            if contrast_factor != 1.0:
                enh = ImageEnhance.Contrast(img)
                img = enh.enhance(contrast_factor)

            # Sharpen
            if sharpen:
                img = img.filter(ImageFilter.SHARPEN)

            # Text
            if text:
                img = add_text(img, text, text_corner, text_size, text_color)

            os.makedirs(output_folder, exist_ok=True)
            base = os.path.basename(image_path)
            name, ext = os.path.splitext(base)
            out_path = os.path.join(output_folder, f"{name}_modositott{ext}")
            img.save(out_path)
            print(f"Kesz: {out_path}")
            return out_path

    except Exception as e:
        print(f"Hiba ({image_path}): {e}")
        return None


def add_text(img, text, corner, size, color):
    img = img.convert("RGB")
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
    else:  # jobb_also
        x, y = iw - w - pad, ih - h - pad

    draw.text((x, y), text, fill=color, font=font)
    return img


def process_folder(folder, config):
    paths = []
    for f in os.listdir(folder):
        _, ext = os.path.splitext(f.lower())
        if ext in SUPPORTED_EXTS:
            paths.append(os.path.join(folder, f))

    print(f"{len(paths)} kep talalva a mappaban")
    for p in paths:
        modify_image(p, **config)


def process_multiple_images(paths, config):
    print(f"{len(paths)} kep feldolgozasa indult")
    for p in paths:
        print(f"Kep: {p}")
        modify_image(p, **config)
