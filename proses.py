import os
from datetime import date, datetime

import streamlit as st

from cuaca import ambil_data
from jadwal import cek_nama_kota, rangkai_hasil, teks_ke_menit


NAMA_APP = "TIDE"
TAGLINE = "Catch the right time, every day"
FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(FOLDER, "assets", "logo.jpeg")
HALAMAN_LOGIN = "app.py"
HALAMAN_SUSUN = "pages/susun_jadwal.py"
HALAMAN_HASIL = "pages/hasil_jadwal.py"
HALAMAN_EKSPOR = "pages/ekspor.py"

def siapkan_state():
    awal = {"pengguna": None,        
            "cache": {},            
            "hasil": None,          
            "pdf_bytes": None}       
    for nama, nilai in awal.items():
        if nama not in st.session_state:
            st.session_state[nama] = nilai


def keluar():
    for nama in ["pengguna", "hasil", "pdf_bytes"]:
        st.session_state[nama] = None


def sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] * { font-weight: 700 !important; font-size: 18px !important; }
        [data-testid="stSidebarLogo"] { height: 6rem !important; max-width: 100% !important; }
[data-testid="stSidebarHeader"] { height: auto !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        if st.session_state.pengguna:
            st.markdown(f"👤 Masuk sebagai **{st.session_state.pengguna}**")
            hasil = st.session_state.hasil
            if hasil:
                st.caption(f"Jadwal terbuka: {hasil['kota']}, {hasil['tanggal']}")
            st.button("Keluar", on_click=keluar, width="stretch")
        else:
            st.caption("Belum login.")


def siapkan_halaman(perlu_login=True):
    st.set_page_config(page_title=NAMA_APP, page_icon=LOGO, layout="wide")
    siapkan_state()
    st.logo(LOGO, size="large")
    sidebar()
    if perlu_login and not st.session_state.pengguna:
        st.warning("Silakan login atau register dulu.")
        st.page_link(HALAMAN_LOGIN, label="Ke halaman Login", icon="🔑")
        st.stop()


def butuh_hasil():
    hasil = st.session_state.hasil
    if hasil is None:
        st.info("Belum ada jadwal. Buat dulu di halaman **Susun Jadwal**, atau buka jadwal lama di **Riwayat**.")
        st.page_link(HALAMAN_SUSUN, label="Ke Susun Jadwal", icon="🗓️")
        st.stop()
    return hasil

def buat_jadwal(kota, tanggal, jam_mulai, jam_selesai, kegiatan):
    kota = cek_nama_kota(kota)
    lokasi, per_jam, harian = ambil_data(kota, tanggal, st.session_state.cache)
    sekarang_menit = None
    if tanggal == date.today():
        now = datetime.now()
        sekarang_menit = now.hour * 60 + now.minute
    hasil = rangkai_hasil(st.session_state.pengguna, lokasi, tanggal, per_jam, harian,
                          teks_ke_menit(jam_mulai), teks_ke_menit(jam_selesai), kegiatan, sekarang_menit)
    return hasil

