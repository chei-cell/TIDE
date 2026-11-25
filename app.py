import streamlit as st

import akun
from proses import HALAMAN_SUSUN, LOGO, NAMA_APP, TAGLINE, siapkan_halaman

siapkan_halaman(perlu_login=False)

kiri, kanan = st.columns([1, 2])
with kiri:
    st.image(LOGO, width="stretch")
with kanan:
    st.title(NAMA_APP)
    st.subheader(TAGLINE)
    st.write("Tulis kegiatan yang ingin dilakukan hari ini, berapa lama, dan seberapa prioritas kegiatan tersebut. "
             "TIDE membaca cuaca per jam, dan akan menyusun jam yang paling pas untuk setiap kegiatan "
             "AI menjelaskan jadwalnya dan siap menjawab pertanyaan tentang cuaca hari itu.")

pengguna = st.session_state.pengguna
if pengguna:
    st.success(f"Halo, **{pengguna}**! Anda sudah login.")
    st.page_link(HALAMAN_SUSUN, label="Mulai susun jadwal hari ini", icon="🗓️")

    st.markdown("### Cara menggunakan TIDE")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**1. Isi kegiatan**\n\nKota, tanggal, jam mulai-selesai, lalu daftar kegiatan "
                "beserta jenis, durasi, dan prioritasnya.")
    c2.markdown("**2. Lihat jadwal**\n\nTIDE menyusun jam terbaik untuk tiap kegiatan, "
                "lengkap dengan ringkasan cuaca, grafik, dan penjelasan AI.")
    c3.markdown("**3. Tanya dan simpan**\n\nTanya chatbot cuaca, lalu unduh ringkasan di halaman Ekspor (PDF, Excel, JSON). "
                "Semua jadwal tersimpan di Riwayat.")
    st.stop()

st.markdown("### Masuk ke TIDE")
tab_login, tab_daftar = st.tabs(["Login", "Register"])

with tab_login:
    with st.form("form_login"):
        nama = st.text_input("Nama", max_chars=akun.MAKS_NAMA)
        password = st.text_input("Password", type="password", max_chars=akun.MAKS_PASSWORD)
        masuk = st.form_submit_button("Login", type="primary")
    if masuk:
        try:
            st.session_state.pengguna = akun.login(nama, password)
            st.session_state.hasil = None
            st.rerun()
        except ValueError as e:
            st.error(str(e))

with tab_daftar:
    with st.form("form_register"):
        nama_baru = st.text_input("Nama", max_chars=akun.MAKS_NAMA,
                                  help=f"{akun.MIN_NAMA}-{akun.MAKS_NAMA} karakter: huruf, angka, spasi, titik, - atau _.")
        pass_baru = st.text_input("Password", type="password", max_chars=akun.MAKS_PASSWORD,
                                  help=f"Minimal {akun.MIN_PASSWORD} karakter.")
        pass_ulang = st.text_input("Ulangi password", type="password", max_chars=akun.MAKS_PASSWORD)
        daftar = st.form_submit_button("Register", type="primary")
    if daftar:
        try:
            st.session_state.pengguna = akun.register(nama_baru, pass_baru, pass_ulang)
            st.session_state.hasil = None
            st.rerun()
        except ValueError as e:
            st.error(str(e))
    st.caption("mohon jangan memakai password yang sama dengan akun penting Anda.")