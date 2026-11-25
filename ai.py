import os
import tomllib

import requests


PENGATURAN_AWAL = {
    "LOKAL_URL" : "http://127.0.0.1:8888/v1", 
    "LOKAL_MODEL" : "Qwen3.5-4B-Q8_0:Q8_0",      
    "LOKAL_API_KEY" :  " ",         
    "LOKAL_TIMEOUT" : 180,
    "LOKAL_MAKS_TOKEN" : 700,                       
}
NAMA_QWEN = "Qwen 3.5-4B lokal"


ATURAN = ("Kamu asisten penjadwal kegiatan harian aplikasi TIDE. Jawab dalam bahasa Indonesia sehari-hari, "
          "singkat dan praktis. Gunakan HANYA data yang diberikan. Jangan mengubah jam pada jadwal, "
          "karena jadwal sudah dihitung oleh aplikasi.")

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_SECRETS = os.path.join(FOLDER, ".streamlit", "secrets.toml")

def cari_file_secrets():
    if os.path.exists(FILE_SECRETS):
        return FILE_SECRETS
    return None


def baca_file_secrets():
    path = cari_file_secrets()
    if path is None:
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def baca_pengaturan(nama):
    isi = baca_file_secrets()
    return isi.get(nama, PENGATURAN_AWAL[nama])


def bersihkan_jawaban(teks):
    if "</think>" in teks:
        teks = teks.split("</think>")[-1]
    return teks.replace("<think>", "").strip()


def header_lokal():
    key = str(baca_pengaturan("LOKAL_API_KEY")).strip()
    if key:
        return {"Authorization": "Bearer " + key}
    return {}


def server_lokal_siap():
    url = str(baca_pengaturan("LOKAL_URL")).rstrip("/") + "/models"
    try:
        return requests.get(url, headers=header_lokal(), timeout=3).status_code == 200
    except requests.exceptions.RequestException:
        return False


def kirim_pesan_qwen(pesan):
    alamat = str(baca_pengaturan("LOKAL_URL")).rstrip("/")
    url = alamat + "/chat/completions"
    isi = {
        "model": baca_pengaturan("LOKAL_MODEL"),
        "messages": pesan,
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 20,
        "min_p": 0.0,
        "presence_penalty": 1.5,
        "max_tokens": int(baca_pengaturan("LOKAL_MAKS_TOKEN")),
        "chat_template_kwargs": {"enable_thinking": False},
    }
    try:
        jawaban = requests.post(url, json=isi, headers=header_lokal(),
                                timeout=float(baca_pengaturan("LOKAL_TIMEOUT")))
    except requests.exceptions.ConnectionError:
        raise ValueError(f"Server Qwen lokal tidak bisa dihubungi di {alamat}. Nyalakan Unsloth Studio, pilih model "
                         "Qwen, dan pastikan LOKAL_URL di .streamlit/secrets.toml sama dengan alamat Studio.")
    except requests.exceptions.Timeout:
        raise ValueError("Qwen lokal terlalu lama menjawab. Naikkan LOKAL_TIMEOUT atau kecilkan LOKAL_MAKS_TOKEN.")
    if jawaban.status_code in (401, 403):
        raise ValueError("Server menolak API key. Cek LOKAL_API_KEY (Unsloth Studio: Settings > API).")
    if jawaban.status_code != 200:
        raise ValueError(f"Server Qwen menolak permintaan (kode {jawaban.status_code}). Cek LOKAL_MODEL "
                         f"(sekarang: {baca_pengaturan('LOKAL_MODEL')}). Isi server: {jawaban.text[:200]}")
    try:
        teks = jawaban.json()["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise ValueError("Jawaban server Qwen tidak bisa dibaca.")
    teks = bersihkan_jawaban(teks or "")
    if not teks:
        raise ValueError("Qwen tidak memberi jawaban.")
    return teks


def panggil_qwen(prompt):
    """Kirim satu prompt (dengan ATURAN) ke Qwen lokal."""
    return kirim_pesan_qwen([{"role": "system", "content": ATURAN}, {"role": "user", "content": prompt}])

