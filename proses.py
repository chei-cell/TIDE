import os

import streamlit as st 

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
