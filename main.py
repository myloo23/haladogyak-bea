import re
from processor import modify_image, process_folder, process_multiple_images


def parse_resize_input(raw: str):
    raw = raw.strip()
    if not raw:
        return None
    nums = list(map(int, re.findall(r"-?\d+", raw)))
    if len(nums) != 2:
        raise ValueError("Atmeretezeshez 2 szam kell (szelesseg, magassag).")
    return (nums[0], nums[1])


def parse_crop_input(raw: str):
    """
    Elfogad:
    - 4 számot: (bal, felso, jobb, also) vagy (bal, felso, szel, mag) autodetektálva a processorban
    - 2 számot: (szel, mag) -> sarokhoz rögzített kivágás
    - Szöveges sarok + 2 szám:
        "bal felso 800 600"
        "jobb also 800 600"
    """
    raw_l = raw.strip().lower()
    if not raw_l:
        return None

    nums = list(map(int, re.findall(r"-?\d+", raw_l)))

    # sarok felismerése
    corner = None
    if "bal" in raw_l and "felso" in raw_l:
        corner = "bal_felso"
    elif "jobb" in raw_l and "felso" in raw_l:
        corner = "jobb_felso"
    elif "bal" in raw_l and ("also" in raw_l or "alsó" in raw_l):
        corner = "bal_also"
    elif "jobb" in raw_l and ("also" in raw_l or "alsó" in raw_l):
        corner = "jobb_also"

    # 4 szám esetén: standard PIL / vagy (bal, felso, szel, mag)
    if len(nums) == 4:
        return tuple(nums)

    # 2 szám esetén: sarok + méret
    if len(nums) == 2:
        w, h = nums
        return {"mode": "anchor", "corner": corner or "bal_felso", "width": w, "height": h}

    raise ValueError("A kivagashoz 2 vagy 4 szamot adj meg.")


def get_config():
    config = {}

    out = input("Kimeneti mappa neve: ")
    config["output_folder"] = out if out else "modositott_kepek"

    g = input("Legyen szurke? (igen/nem): ")
    config["grayscale"] = (g.strip().lower() == "igen")

    r = input("Forgatas fokban, ures ha nincs: ")
    config["rotate_angle"] = int(r) if r else 0

    s = input("Atmeretezes (pl. 800,600) vagy ures: ")
    if s:
        try:
            config["resize_dims"] = parse_resize_input(s)
        except:
            print("Hibas atmeretezes formatum, kihagyom.")
            config["resize_dims"] = None
    else:
        config["resize_dims"] = None

    c = input(
        "Kivagas peldak:\n"
        "  - 10,20,300,400\n"
        "  - 100 100 200 150\n"
        "  - 800 600\n"
        "  - bal felso 800 600\n"
        "Add meg vagy ures: "
    )
    if c:
        try:
            config["crop_box"] = parse_crop_input(c)
        except Exception:
            print("Hibas kivagas formatum, kihagyom.")
            config["crop_box"] = None
    else:
        config["crop_box"] = None

    b = input("Fenyero faktor (1.0 alap): ")
    config["brightness_factor"] = float(b) if b else 1.0

    ct = input("Kontraszt faktor (1.0 alap): ")
    config["contrast_factor"] = float(ct) if ct else 1.0

    sh = input("Elesites? (igen/nem): ")
    config["sharpen"] = (sh.strip().lower() == "igen")

    t = input("Felirat vagy ures: ")
    config["text"] = t if t else None

    if t:
        cor = input("Sarok (bal_felso, jobb_felso, bal_also, jobb_also): ")
        config["text_corner"] = cor if cor else "bal_felso"
        ts = input("Betumeret (alap 40): ")
        config["text_size"] = int(ts) if ts else 40

    return config


def main():
    mode = input("Egy kep, tobb kep vagy mappa? (kep/tobb/mappa): ").strip().lower()
    config = get_config()

    if mode == "kep":
        path = input("Kep eleresi utja: ")
        modify_image(path, **config)

    elif mode == "tobb":
        print("Add meg a kepek eleresi utjait vesszovel elvalasztva")
        lista = input("Utjak: ")
        paths = [p.strip() for p in lista.split(",") if p.strip()]
        process_multiple_images(paths, config)

    else:
        folder = input("Mappa neve: ")
        process_folder(folder, config)


if __name__ == "__main__":
    main()
