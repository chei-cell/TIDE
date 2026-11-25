import math

jenis = ["Luar ruangan", "Dalam ruangan"]

bobot_jenis = {
    "Luar ruangan" : {"hujan" : 40, "suhu_nyaman" : 15, "uv_rendah" : 15, "pm25"  : 10, "angin_pelan" : 5, "terang" : 15},
}

batas_hujan = 70

kolom = {
    "hujan" : "hujan",
    "uv_rendah" : "uv",
    "angin_pelan" : "angin",
    "suhu_nyaman" : "suhu",
    "pm25" : "pm25",
    "terang" : "siang",
}

def batas(nilai):
    return max(0.0, min(100.0, nilai))

def linear(v, buruk, bagus):
    return batas((v - buruk) / (bagus - buruk) * 100)

def rentang(v, buruk_bawah, bagus_bawah, bagus_atas, buruk_atas):
    if v < bagus_bawah:
        return linear(v, buruk_bawah, bagus_bawah)
    elif v > bagus_atas:
        return linear(v, buruk_atas, bagus_atas)
    return 100.0

def faktor(nama, v):
    if nama == "hujan":
        return batas(100 - v)
    elif nama == "uv_rendah":
        return linear(v, 11, 2)
    elif nama == "angin_pelan":
        return linear(v, 40, 10)
    elif nama == "suhu_nyaman":
        return rentang(v, 12, 20, 32, 40)
    elif nama == "pm25":
        return linear(v, 75, 15)
    elif nama == "terang":
        if v >= 1:
            return 100.0
        else:
            return 0.0
    return 0.0

def kosong(nilai):
    return nilai is None or (isinstance(nilai, float) and math.isnan(nilai))

def hitung_skor(per_jam, bobot):
    hasil = []
    for baris in per_jam:
        total = 0.0
        bobot_dipakai = 0.0
        for nama_faktor, b in bobot.items():
            nilai = baris.get(kolom[nama_faktor])
            if kosong(nilai):
                continue
            total += b * faktor(nama_faktor, nilai)
            bobot_dipakai += b
        if bobot_dipakai > 0:
            skor = total / bobot_dipakai
        else:
            skor = 0.0
        if not kosong(baris.get("hujan")) and baris["hujan"] >= batas_hujan:
            skor = min(skor, 30.0)
        hasil.append(round(skor, 1))
    return hasil

def skor_semua_kegiatan(per_jam):
    luar_ruangan = hitung_skor(per_jam, bobot_jenis["Luar ruangan"])
    dalam_ruangan = []
    for d in luar_ruangan:
        dalam_ruangan.append(round(100 - d, 1))
    return {"Luar ruangan" : luar_ruangan,
            "Dalam ruangan" : dalam_ruangan}

def label(skor):
    if skor >= 70:
        return "baik"
    elif skor >= 40:
        return "cukup"
    return "buruk"