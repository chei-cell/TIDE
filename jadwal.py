import math
from datetime import datetime
import pandas as pd
from algoritma import cari_rentang_kosong_terbaik, quick_sort
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


def urutkan_kegiatan(daftar):
    """QUICK SORT: prioritas tinggi dulu; jika sama, durasi lebih lama dulu; jika masih sama, urutan input.

    Nilai urut = prioritas x 10000 + durasi (menit) - nomor/100.
    Durasi paling lama 1440 menit (< 10000), jadi prioritas selalu menang atas durasi.
    """
    data = []
    for k in daftar:
        salinan = dict(k)
        salinan["nilai_urut"] = PRIORITAS[k["prioritas"]] * 10000 + k["durasi_menit"] - k["nomor"] / 100
        data.append(salinan)
    return quick_sort(data, "nilai_urut")


def skor_per_slot(skor_jam):
    """Ubah 24 skor per jam menjadi 96 skor per slot 15 menit (slot memakai skor jamnya)."""
    hasil = []
    for slot in range(SLOT_SEHARI):
        hasil.append(skor_jam[slot * MENIT_SLOT // 60])
    return hasil


def tandai_slot(mulai_menit, selesai_menit):
    """List True/False sepanjang 96 slot. True = slot di luar jam mulai-selesai (tidak boleh dipakai)."""
    mulai_slot = mulai_menit // MENIT_SLOT
    selesai_slot = selesai_menit // MENIT_SLOT
    terisi = []
    for slot in range(SLOT_SEHARI):
        terisi.append(slot < mulai_slot or slot >= selesai_slot)
    return terisi

def isi_jadwal(k, mulai, rata2):
    """Satu baris jadwal (dictionary) untuk kegiatan k yang mulai pada menit 'mulai'."""
    selesai = mulai + k["durasi_menit"]
    skor = round(rata2, 1)
    kategori = label(skor)
    if k["jenis"] == "Dalam ruangan":
        kategori = "aman (di dalam)"     
    return {"nama": k["nama"], "jenis": k["jenis"], "prioritas": k["prioritas"],
            "durasi_menit": k["durasi_menit"], "mulai_menit": mulai, "selesai_menit": selesai,
            "mulai": menit_ke_teks(mulai), "selesai": menit_ke_teks(selesai),
            "skor": skor, "kategori": kategori}


def susun_jadwal(kegiatan, skor_jenis, mulai_menit, selesai_menit):
    """Susun jadwal tanpa bentrok.

    kegiatan   : list of dictionary dari buat_kegiatan()
    skor_jenis : {jenis: list 24 skor per jam}
    Hasil: (jadwal, tidak_muat)
      jadwal     = list of dictionary, urut dari jam mulai paling pagi
      tidak_muat = list kegiatan yang tidak mendapat tempat
    """
    terisi = tandai_slot(mulai_menit, selesai_menit)

    slot_jenis = {}    
    for jenis, skor_jam in skor_jenis.items():
        slot_jenis[jenis] = skor_per_slot(skor_jam)

    jadwal = []
    tidak_muat = []
    for k in urutkan_kegiatan(kegiatan):
        panjang = int(math.ceil(k["durasi_menit"] / MENIT_SLOT))
        hasil = cari_rentang_kosong_terbaik(slot_jenis[k["jenis"]], terisi, panjang)
        if hasil is None:
            tidak_muat.append({"nama": k["nama"], "jenis": k["jenis"], "prioritas": k["prioritas"],
                               "durasi_menit": k["durasi_menit"],
                               "alasan": "Tidak ada jam kosong yang cukup panjang."})
            continue
        awal = hasil["awal"]
        for slot in range(awal, awal + panjang):
            terisi[slot] = True
        jadwal.append(isi_jadwal(k, awal * MENIT_SLOT, hasil["rata2"]))
    return quick_sort(jadwal, "mulai_menit", menaik=True), tidak_muat

def rangkai_hasil(pengguna, lokasi, tanggal, per_jam, harian, mulai_menit, selesai_menit, kegiatan,
                  sekarang_menit=None):
    """Gabungkan semuanya menjadi satu dictionary hasil (bisa langsung disimpan ke JSON).

    sekarang_menit: jika tanggal = hari ini, jam yang sudah lewat tidak dipakai.
    Ringkasan cuaca masih None (dibuat di Tahap 3).
    """
    if selesai_menit - mulai_menit < MENIT_SLOT:
        raise ValueError("Jam selesai harus lebih lambat dari jam mulai.")
    catatan = []
    mulai_efektif = mulai_menit
    if sekarang_menit is not None and sekarang_menit > mulai_menit:
        mulai_efektif = bulat_ke_atas(sekarang_menit)
        if mulai_efektif >= selesai_menit:
            raise ValueError("Jam yang dipilih untuk hari ini sudah lewat. Pilih jam selesai yang lebih malam "
                             "atau tanggal lain.")
        catatan.append(f"Hari ini sudah lewat jam {menit_ke_teks(mulai_menit)}, jadi jadwal dimulai paling "
                       f"cepat {menit_ke_teks(mulai_efektif)}.")

    total = 0
    for k in kegiatan:
        total += k["durasi_menit"]
    tersedia = selesai_menit - mulai_efektif
    if total > tersedia:
        catatan.append(f"Total durasi kegiatan ({teks_durasi(total)}) lebih lama dari waktu yang tersedia "
                       f"({teks_durasi(tersedia)}). Kegiatan prioritas rendah mungkin tidak terjadwal.")

    skor_jenis = skor_semua_jenis(per_jam)
    jadwal, tidak_muat = susun_jadwal(kegiatan, skor_jenis, mulai_efektif, selesai_menit)

    sekarang = datetime.now()
    return {
        "id": sekarang.strftime("%Y%m%d%H%M%S%f"),
        "dibuat": sekarang.strftime("%Y-%m-%d %H:%M"),
        "pengguna": pengguna,
        "kota": lokasi["nama"], "label_kota": lokasi.get("label", lokasi["nama"]),
        "tanggal": tanggal.isoformat(),
        "jam_mulai": menit_ke_teks(mulai_menit), "jam_selesai": menit_ke_teks(selesai_menit),
        "kegiatan": kegiatan,
        "jadwal": jadwal,
        "tidak_terjadwal": tidak_muat,
        "catatan": catatan,
        "cuaca": None,                      
        "per_jam": per_jam,
        "harian": harian,
        "skor_jenis": skor_jenis,
        "saran": None, "sumber": None,
        "chat": [],
    }


def tabel_jadwal(hasil):
    baris = []
    for j in hasil["jadwal"]:
        baris.append({"Jam": f"{j['mulai']}-{j['selesai']}", "Kegiatan": j["nama"], "Jenis": j["jenis"],
                      "Prioritas": j["prioritas"], "Durasi": teks_durasi(j["durasi_menit"]),
                      "Skor": j["skor"], "Kategori": j["kategori"], "Cuaca saat itu": j.get("cuaca", "-")})
    return pd.DataFrame(baris)