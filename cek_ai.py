import ai

path = ai.cari_file_secrets()
if path is None:
    print("PERINGATAN  : secrets.toml TIDAK DITEMUKAN. Seharusnya ada di:")
    print("              " + ai.FILE_SECRETS)
    print("              Salin .streamlit/secrets.toml.example menjadi .streamlit/secrets.toml lalu isi.")
else:
    print("File secrets:", path)
print("LOKAL_URL   :", ai.baca_pengaturan("LOKAL_URL"))
print("LOKAL_MODEL :", ai.baca_pengaturan("LOKAL_MODEL"))
key = str(ai.baca_pengaturan("LOKAL_API_KEY"))
print("API key     :", (key[:14] + "...") if key else "(kosong)")
print("Server siap :", ai.server_lokal_siap())
try:
    print("Jawaban AI  :", ai.panggil_qwen("Jawab satu kata saja: siap?"))
except ValueError as e:
    print("GAGAL       :", e)
