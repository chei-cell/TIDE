from datetime import date, timedelta

import streamlit as st

from jadwal import MAKS_KEGIATAN, MAKS_NAMA, PRIORITAS, buat_kegiatan, durasi_ke_menit, pilihan_jam
from proses import HALAMAN_HASIL, NAMA_APP, TAGLINE, buat_jadwal, siapkan_halaman
from skor import JENIS

siapkan_halaman()

tersimpan = st.session_state.setdefault("isian_tersimpan", {})


def ingat(kunci, awal):
    if kunci not in st.session_state:
        st.session_state[kunci] = tersimpan.get(kunci, awal)
    return kunci


st.markdown(f"## 🗓️ {NAMA_APP}")
st.caption(TAGLINE)
st.subheader("Silahkan susun jadwal kamu hari ini")

st.markdown("#### 1. Hari dan tempat")
k1, k2 = st.columns(2)
kota = k1.text_input("Kota", max_chars=60, key=ingat("kota", "Yogyakarta"),
                     help="Boleh diperjelas dengan provinsi, misalnya 'Pati, Jawa Tengah'.")
hari_ini = date.today()
if tersimpan.get("tanggal") and tersimpan["tanggal"] < hari_ini:
    tersimpan["tanggal"] = hari_ini               
tanggal = k2.date_input("Tanggal", min_value=hari_ini,
                        max_value=hari_ini + timedelta(days=15), key=ingat("tanggal", hari_ini))
j1, j2 = st.columns(2)
jam_mulai = j1.selectbox("Jam mulai", pilihan_jam()[:-1], key=ingat("jam_mulai", "07:00"),
                         help="Kegiatan paling awal dimulai jam ini.")
jam_selesai = j2.selectbox("Jam selesai", pilihan_jam()[1:], key=ingat("jam_selesai", "21:00"),
                           help="Semua kegiatan selesai paling lambat jam ini.")

st.markdown("#### 2. Kegiatan")
jumlah = st.number_input("Jumlah kegiatan", min_value=1, max_value=MAKS_KEGIATAN, step=1, key=ingat("jumlah", 3))
with st.expander("Arti jenis kegiatan"):
    st.markdown("- **Luar ruangan**: olahraga, jalan kaki, menjemur, berkebun, perjalanan/berkendara. "
                "Dicarikan jam yang kering, suhunya nyaman, dan tidak terlalu terik.\n"
                "- **Dalam ruangan**: belajar, rapat, memasak. Diletakkan pada jam yang cuacanya kurang baik, "
                "supaya jam cerah tersisa untuk kegiatan luar ruangan.")

isian = []  
for i in range(int(jumlah)):
    with st.container(border=True):
        st.markdown(f"**Kegiatan {i + 1}**")
        a, b, c = st.columns([3, 2, 2])
        nama = a.text_input("Nama kegiatan", key=ingat(f"nama_{i}", ""), max_chars=MAKS_NAMA,
                            placeholder="Contoh: Lari pagi, Menjemur, Kerja kelompok")
        jenis = b.selectbox("Jenis", JENIS, key=ingat(f"jenis_{i}", JENIS[0]))
        prioritas = c.selectbox("Prioritas", list(PRIORITAS.keys()), key=ingat(f"prioritas_{i}", "Sedang"))
        d, e = st.columns([1, 4])
        satuan = d.radio("Satuan durasi", ["menit", "jam"], key=ingat(f"satuan_{i}", "jam"), horizontal=True)
        if satuan == "menit":
            nilai = e.slider("Durasi (menit)", 15, 180, step=15, key=ingat(f"durasi_{i}_menit", 60))
        else:
            nilai = e.slider("Durasi (jam)", 0.5, 12.0, step=0.5, key=ingat(f"durasi_{i}_jam", 1.0))
        isian.append({"nomor": i + 1, "nama": nama, "jenis": jenis, "prioritas": prioritas,
                      "durasi_menit": durasi_ke_menit(nilai, satuan)})

# simpan semua isian widget di halaman ini
for kunci in list(st.session_state.keys()):
    if kunci in ("kota", "tanggal", "jam_mulai", "jam_selesai", "jumlah") or kunci.startswith(
            ("nama_", "jenis_", "prioritas_", "satuan_", "durasi_")):
        tersimpan[kunci] = st.session_state[kunci]

st.caption("Penyusunan dari proritas tinggi dulu, jika prioritas sama kegiatan yang druasinya lebih lama akan didahulukan")
if st.button("Susun jadwal", type="primary", width="stretch"):
    try:
        kegiatan = []
        for c in isian:
            kegiatan.append(buat_kegiatan(c["nomor"], c["nama"], c["jenis"], c["durasi_menit"], c["prioritas"]))
        with st.spinner("Mengambil data cuaca dan menyusun jadwal..."):
            st.session_state.hasil = buat_jadwal(kota, tanggal, jam_mulai, jam_selesai, kegiatan)
            st.session_state.pdf_bytes = None
    except ValueError as e:
        st.error(str(e))
    else:
        st.switch_page(HALAMAN_HASIL)
