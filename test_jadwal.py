from datetime import date
from bantuan_tes import HARIAN, LOKASI, contoh_hasil, cuaca_contoh, harus_gagal, jalankan_tes
from jadwal import (buat_kegiatan, cek_nama_kota, durasi_ke_menit, menit_ke_teks, pilihan_jam, rangkai_hasil,
                    susun_jadwal, teks_durasi, teks_ke_menit)
from skor import BOBOT_JENIS, hitung_skor, skor_semua_jenis

def test_skor():
    for bobot in BOBOT_JENIS.values():
        assert sum(bobot.values()) == 100
    kering = cuaca_contoh()
    basah = cuaca_contoh(jam_hujan=range(24))
    assert hitung_skor(kering, BOBOT_JENIS["Luar ruangan"])[8] > hitung_skor(basah, BOBOT_JENIS["Luar ruangan"])[8]
    assert hitung_skor(basah, BOBOT_JENIS["Luar ruangan"])[8] <= 30 
    semua = skor_semua_jenis(kering)
    for jam in range(24):
        assert abs(semua["Luar ruangan"][jam] + semua["Dalam ruangan"][jam] - 100) < 0.01
    data = cuaca_contoh()
    data[8]["pm25"] = None                                   
    assert hitung_skor(data, BOBOT_JENIS["Luar ruangan"])[8] > 0


def test_waktu():
    assert teks_ke_menit("07:30") == 450 and menit_ke_teks(450) == "07:30" and menit_ke_teks(1440) == "24:00"
    jam = pilihan_jam()
    assert jam[0] == "00:00" and jam[-1] == "24:00" and len(jam) == 97
    assert durasi_ke_menit(1.5, "jam") == 90 and durasi_ke_menit(45, "menit") == 45
    assert teks_durasi(95) == "1 jam 35 menit" and teks_durasi(60) == "1 jam" and teks_durasi(30) == "30 menit"


def test_buat_kegiatan():
    k = buat_kegiatan(1, "  Lari   pagi ", "Luar ruangan", 60, "Tinggi")
    assert k == {"nomor": 1, "nama": "Lari pagi", "jenis": "Luar ruangan", "durasi_menit": 60, "prioritas": "Tinggi"}
    harus_gagal(buat_kegiatan, 1, "   ", "Luar ruangan", 60, "Tinggi")
    harus_gagal(buat_kegiatan, 1, "Lari", "Terbang", 60, "Tinggi")
    harus_gagal(buat_kegiatan, 1, "Lari", "Luar ruangan", 60, "Darurat")
    harus_gagal(buat_kegiatan, 1, "x" * 41, "Luar ruangan", 60, "Tinggi")
    harus_gagal(buat_kegiatan, 1, "Lari", "Luar ruangan", 5, "Tinggi")
    assert cek_nama_kota("  Pati, Jawa Tengah ") == "Pati, Jawa Tengah"
    harus_gagal(cek_nama_kota, "J")
    harus_gagal(cek_nama_kota, "Kota123")

def test_jadwal_di_dalam_rentang_dan_tidak_bentrok():
    kegiatan = [buat_kegiatan(1, "Lari", "Luar ruangan", 60, "Tinggi"),
                buat_kegiatan(2, "Belajar", "Dalam ruangan", 120, "Sedang"),
                buat_kegiatan(3, "Menjemur", "Luar ruangan", 45, "Rendah")]
    jadwal, tidak = susun_jadwal(kegiatan, skor_semua_jenis(cuaca_contoh()), 7 * 60, 21 * 60)
    assert len(jadwal) == 3 and tidak == []
    for i in range(len(jadwal) - 1):                         
        assert jadwal[i]["selesai_menit"] <= jadwal[i + 1]["mulai_menit"]
    for j in jadwal:
        assert 7 * 60 <= j["mulai_menit"] and j["selesai_menit"] <= 21 * 60
        assert 0 <= j["skor"] <= 100

def test_rangkai_hasil_dasar():
    kegiatan = [buat_kegiatan(1, "Lari", "Luar ruangan", 60, "Tinggi")]
    hasil = rangkai_hasil("Valine", LOKASI, date(2026, 11, 25), cuaca_contoh(), HARIAN, 6 * 60, 20 * 60, kegiatan)
    for kunci in ["id", "pengguna", "kota", "label_kota", "tanggal", "jam_mulai", "jam_selesai", "kegiatan",
                  "jadwal", "tidak_terjadwal", "catatan", "cuaca", "per_jam", "harian", "skor_jenis",
                  "saran", "sumber", "chat"]:
        assert kunci in hasil, kunci
    assert hasil["jam_mulai"] == "06:00" and hasil["jadwal"][0]["nama"] == "Lari"
    harus_gagal(rangkai_hasil, "A", LOKASI, date(2026, 11, 25), cuaca_contoh(), HARIAN, 600, 600, kegiatan)


def test_quick_sort():
    from algoritma import quick_sort
    data = [{"v": v} for v in [5, 3, 9, 3, 1, 9, 0, 7]]
    assert [d["v"] for d in quick_sort(data, "v")] == [9, 9, 7, 5, 3, 3, 1, 0]
    assert [d["v"] for d in quick_sort(data, "v", menaik=True)] == [0, 1, 3, 3, 5, 7, 9, 9]
    assert quick_sort([], "v") == []
    assert [d["v"] for d in data] == [5, 3, 9, 3, 1, 9, 0, 7]   # list asli tidak berubah


def test_cari_rentang_kosong():
    from algoritma import cari_indeks, cari_rentang_kosong_terbaik
    skor = [10, 50, 90, 90, 40, 80, 80, 80]
    kosong = [False] * 8
    assert cari_rentang_kosong_terbaik(skor, kosong, 2) == {"awal": 2, "rata2": 90.0}
    terisi = [False, False, True, False, False, False, False, False]
    assert cari_rentang_kosong_terbaik(skor, terisi, 2)["awal"] == 5
    assert cari_rentang_kosong_terbaik(skor, [True] * 8, 1) is None
    assert cari_rentang_kosong_terbaik(skor, kosong, 9) is None
    assert cari_indeks([{"id": "a"}, {"id": "b"}], "id", "b") == 1
    assert cari_indeks([], "id", "b") == -1


if __name__ == "__main__":
    print("Selesai. Gagal:", jalankan_tes(globals()))