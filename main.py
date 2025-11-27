from processor import modify_image, process_folder
from processor import modify_image, process_folder, process_multiple_images


def get_config():
    config = {}

    out = input("Kimeneti mappa neve: ")
    config["output_folder"] = out if out else "modositott_kepek"

    g = input("Legyen szurke? (igen/nem): ")
    config["grayscale"] = g == "igen"

    r = input("Forgatas fokban, ures ha nincs: ")
    config["rotate_angle"] = int(r) if r else 0

    s = input("Atmeretezes szelesseg,magassag vagy ures: ")
    if s:
        try:
            w, h = map(int, s.split(","))
            config["resize_dims"] = (w, h)
        except:
            config["resize_dims"] = None
    else:
        config["resize_dims"] = None

    c = input("Kivagas bal,felso,jobb,also vagy ures: ")
    if c:
        try:
            l, t, r2, b = map(int, c.split(","))
            config["crop_box"] = (l, t, r2, b)
        except:
            config["crop_box"] = None
    else:
        config["crop_box"] = None

    b = input("Fenyero faktor (1.0 alap): ")
    config["brightness_factor"] = float(b) if b else 1.0

    ct = input("Kontraszt faktor (1.0 alap): ")
    config["contrast_factor"] = float(ct) if ct else 1.0

    sh = input("Elesites? (igen/nem): ")
    config["sharpen"] = sh == "igen"

    t = input("Felirat vagy ures: ")
    config["text"] = t if t else None

    if t:
        cor = input("Sarok (bal_felso, jobb_felso, bal_also, jobb_also): ")
        config["text_corner"] = cor if cor else "bal_felso"
        ts = input("Betumeret: ")
        config["text_size"] = int(ts) if ts else 40

    return config


def main():
    mode = input("Egy kep, tobb kep vagy mappa? (kep/tobb/mappa): ")

    config = get_config()

    if mode == "kep":
        path = input("Kep eleresi utja: ")
        modify_image(path, **config)

    elif mode == "tobb":
        print("Add meg a kepek eleresi utjait vesszovel elvalasztva")
        lista = input("Utjak: ")
        paths = [p.strip() for p in lista.split(",")]
        process_multiple_images(paths, config)

    else:
        folder = input("Mappa neve: ")
        process_folder(folder, config)



if __name__ == "__main__":
    main()
