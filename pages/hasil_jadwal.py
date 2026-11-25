import streamlit as st

from proses import NAMA_APP, TAGLINE, siapkan_halaman

siapkan_halaman()
st.markdown(f"## 📊 {NAMA_APP}")
st.caption(TAGLINE)
st.subheader("Hasil jadwal")
