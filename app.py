import streamlit as st

from proses import LOGO, NAMA_APP, TAGLINE, siapkan_halaman

siapkan_halaman(perlu_login=False)

kiri, kanan = st.columns([1, 2])
with kiri:
    st.image(LOGO, width="stretch")
with kanan:
    st.title(NAMA_APP)
    st.subheader(TAGLINE)
    st.write("Tulis kegiatan yang ingin dilakukan hari ini, berapa lama, dan seberapa penting. "
             "TIDE membaca cuaca per jam, lalu menyusun jam yang paling pas untuk setiap kegiatan "
             "tanpa bentrok. AI menjelaskan jadwalnya dan siap menjawab pertanyaan tentang cuaca hari itu.")

if st.session_state.pengguna:
    st.success(f"Halo, **{st.session_state.pengguna}**! Buka halaman lain lewat menu di sidebar.")
    st.stop()

with st.form("form_masuk_sementara"):
    nama = st.text_input("Nama (sementara, tanpa password)")
    masuk = st.form_submit_button("Masuk", type="primary")
if masuk and nama.strip():
    st.session_state.pengguna = nama.strip()
    st.rerun()
