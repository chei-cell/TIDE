import streamlit as st

from proses import NAMA_APP, TAGLINE, siapkan_halaman

siapkan_halaman(perlu_login=False)
st.markdown(f"## 🌊 {NAMA_APP}")
st.subheader(TAGLINE)

st.markdown("### Filosofi")
st.write(
    "*Tide* berarti pasang surut air laut. Nelayan tidak melawan pasang surut: mereka membaca ritmenya, "
    "lalu berlayar pada saat yang tepat. Cuaca juga naik turun dari jam ke jam. TIDE membantu Anda menyusun "
    "hari supaya setiap kegiatan jatuh pada jam yang paling pas."
)

st.markdown("### Cara TIDE menyusun jadwal")
st.markdown(
    "1. Cuaca per jam diambil dari Open-Meteo, lalu diubah menjadi **skor 0-100** sesuai jenis kegiatan "
    "(luar ruangan atau dalam ruangan). Bobot tiap faktor adalah asumsi kelompok.\n"
    "2. Kegiatan diurutkan dengan **quick sort**: prioritas tinggi dulu, lalu yang paling lama.\n"
    "3. Hari dibagi menjadi slot 15 menit. Untuk tiap kegiatan, TIDE melakukan **searching rentang jam terbaik "
    "yang belum terisi** (linear search), lalu menandai rentang itu sebagai terisi. Jadi tidak ada jadwal bentrok.\n"
    "4. AI (Qwen 3.5-4B lokal) hanya menjelaskan jadwal dan menjawab pertanyaan, tidak menghitung jadwal."
)