import math
from datetime import datetime
import pandas as pd
from skor import JENIS, label, skor_semua_jenis

MENIT_SLOT = 15
SLOT_SEHARI = 24 * 60 // MENIT_SLOT
PRIORITAS = {"Tinggi" : 3, "Sedang": 2, "Rendah": 1}
MAKS_KEGIATAN = 8
MAKS_NAMA = 40

def teks_ke_menit(teks):
    jam, menit = teks.split(":")
    return int(jam) * 60 + int(menit)

def menit_ke_teks(menit):
    return f"{menit // 60:02d}:{menit % 60:02d}"

def pilihan_jam():
    hasil = []
    for m in range(0, 24 * 60 + 1, MENIT_SLOT):
        hasil.append(menit_ke_teks(m))
    return hasil

def durasi_ke_menit(nilai, satuan):
    if satuan == "jam":
        return int(round(float(nilai) * 60))
    return int(nilai)

def teks_durasi(menit):
    jam = menit // 60
    sisa = menit % 60

    if jam and sisa:
        return f"{jam} jam {sisa} menit"
    if jam:
        return f"{jam} jam"
    return f"{sisa} menit"

def bulat_ke_atas(menit):
    return int(math.ceil(menit / MENIT_SLOT)) * MENIT_SLOT

#INPUT
def cek_nama_kota(kota):
    kota = kota.strip()
    if len(kota) < 2 or len(kota) > 60:
        raise ValueError("Nama kota harus 2-60 karakter.")
    for huruf in kota:
        if not (huruf.isalpha() or huruf in " .,'-"):
            raise ValueError("Nama kota hanya boleh berisi huruf.")
    return kota

def buat_kegiatan(nomor, nama, jenis, durasi_menit, prioritas):
    nama = " ".join(str(nama).split()) 
    if not nama:
        raise ValueError(f"Nama kegiatan ke-{nomor} masih kosong.")
    if len(nama) > MAKS_NAMA:
        raise ValueError(f"Nama kegiatan ke-{nomor} terlalu panjang (maksimal {MAKS_NAMA} karakter).")
    if jenis not in JENIS:
        raise ValueError(f"Jenis kegiatan ke-{nomor} tidak dikenal.")
    if prioritas not in PRIORITAS:
        raise ValueError(f"Prioritas kegiatan ke-{nomor} tidak dikenal.")
    if durasi_menit < MENIT_SLOT:
        raise ValueError(f"Durasi kegiatan ke-{nomor} minimal {MENIT_SLOT} menit.")
    return {"nomor": nomor, "nama": nama, "jenis": jenis, "durasi_menit": int(durasi_menit),
            "prioritas": prioritas}