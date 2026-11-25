import streamlit as st

from jadwal import tabel_jadwal, teks_durasi
from proses import NAMA_APP, TAGLINE, butuh_hasil, siapkan_halaman

siapkan_halaman()
st.markdown(f"## 📊 {NAMA_APP}")
st.caption(TAGLINE)

hasil = butuh_hasil()
st.subheader(f"Jadwal {hasil['tanggal']} di {hasil['label_kota']}")
st.caption(f"Rentang hari {hasil['jam_mulai']}-{hasil['jam_selesai']}. Dibuat {hasil['dibuat']}.")

st.markdown("### 🗓️ Jadwal yang disarankan")
for cat in hasil["catatan"]:
    st.warning(cat)
if hasil["jadwal"]:
    st.dataframe(tabel_jadwal(hasil), hide_index=True, width="stretch")
    st.caption("Skor 0-100 = kecocokan cuaca, >= 70 Baik, 40-69 cukup, < 40 buruk). "
               "Kegiatan dalam ruangan karena tidak berpengaruh jadi terkadang diletakkan pada jam yang cuacanya jelek.")
else:
    st.error("Kegiatan nya tidak ada!")
for t in hasil["tidak_terjadwal"]:
    st.error(f"**{t['nama']}** ({teks_durasi(t['durasi_menit'])}, prioritas {t['prioritas']}) tidak terjadwal: "
             f"{t['alasan']} mohon periksa durasi.")
