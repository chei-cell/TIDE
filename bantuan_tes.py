import logging
import os
import tempfile
from datetime import date

LOKASI = {"nama": "Yogyakarta", "label": "Yogyakarta, DI Yogyakarta, Indonesia"}
HARIAN = {"matahari_terbit": "05:20", "matahari_terbenam": "17:50"}


def cuaca_contoh(jam_hujan=()):
    data = []
    for jam in range(24):
        hujan = 90.0 if jam in jam_hujan else 5.0
        data.append({"jam": jam, "kondisi": "Hujan sedang" if jam in jam_hujan else "Cerah berawan",
                     "suhu": 27.0, "terasa": 29.0, "kelembapan": 60.0, "hujan": hujan,
                     "curah_mm": 2.0 if jam in jam_hujan else 0.0, "awan": 30.0, "angin": 8.0,
                     "uv": 5.0 if 9 <= jam <= 15 else 1.0, "siang": 1.0 if 6 <= jam <= 17 else 0.0,
                     "pm25": 12.0})
    return data


def harus_gagal(fungsi, *argumen):
    """Tes lulus hanya jika fungsi(*argumen) melempar ValueError."""
    try:
        fungsi(*argumen)
    except ValueError:
        return
    assert False, "ValueError"


def tmp_file(nama):
    return os.path.join(tempfile.mkdtemp(), nama)


def contoh_hasil():
    from jadwal import buat_kegiatan, rangkai_hasil
    kegiatan = [buat_kegiatan(1, "Lari pagi", "Luar ruangan", 60, "Tinggi"),
                buat_kegiatan(2, "Belajar – UAS 😀", "Dalam ruangan", 120, "Sedang"),
                buat_kegiatan(3, "Menjemur", "Luar ruangan", 45, "Rendah")]
    return rangkai_hasil("Valine", LOKASI, date(2026, 11, 25), cuaca_contoh([13, 14]), HARIAN,
                         7 * 60, 21 * 60, kegiatan)


def jalankan_tes(semua):
    logging.disable(logging.WARNING)       # sembunyikan peringatan Streamlit yang tidak penting saat tes
    gagal = 0
    for nama, fungsi in list(semua.items()):
        if nama.startswith("test_") and callable(fungsi):
            try:
                fungsi()
                print("OK   ", nama)
            except Exception as e:
                gagal += 1
                print("GAGAL", nama, "->", repr(e))
    return gagal
