import json
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_USERS = os.path.join(FOLDER, "users.json")
MIN_NAMA, MAKS_NAMA = 3, 20
MIN_PASSWORD, MAKS_PASSWORD = 4, 30


def muat_users(path=FILE_USERS):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def simpan_users(data, path=FILE_USERS):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def rapikan_nama(nama):
    return " ".join(str(nama).split())


def cek_nama(nama):
    nama = rapikan_nama(nama)
    if len(nama) < MIN_NAMA or len(nama) > MAKS_NAMA:
        raise ValueError(f"Nama harus {MIN_NAMA}-{MAKS_NAMA} karakter.")
    for huruf in nama:
        if not (huruf.isalnum() or huruf in " _-."):
            raise ValueError("Nama hanya boleh berisi huruf, angka, spasi, titik, - dan _.")
    return nama


def cek_password(password):
    if len(password) < MIN_PASSWORD or len(password) > MAKS_PASSWORD:
        raise ValueError(f"Password harus {MIN_PASSWORD}-{MAKS_PASSWORD} karakter.")
    return password


def cari_nama(data, nama):
    dicari = rapikan_nama(nama).lower()
    for n in data.keys():                  # periksa satu per satu dari awal sampai akhir
        if n.lower() == dicari:
            return n
    return None


def register(nama, password, ulang, path=FILE_USERS):
    nama = cek_nama(nama)
    cek_password(password)
    if password != ulang:
        raise ValueError("Ulangi password dengan benar, kedua password belum sama.")
    data = muat_users(path)
    if cari_nama(data, nama) is not None:
        raise ValueError(f"Nama '{nama}' sudah dipakai. Pilih nama lain atau login.")
    data[nama] = password
    simpan_users(data, path)
    return nama


def login(nama, password, path=FILE_USERS):
    data = muat_users(path)
    asli = cari_nama(data, nama)
    if asli is None:
        raise ValueError("Nama belum terdaftar. Silakan register dulu.")
    if data[asli] != password:
        raise ValueError("Password salah.")
    return asli
