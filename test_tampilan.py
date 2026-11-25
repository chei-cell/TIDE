import ai
from bantuan_tes import contoh_hasil, jalankan_tes, tmp_file


def matikan_ai():
    palsu = {"LOKAL_URL": "http://127.0.0.1:9/v1", "LOKAL_TIMEOUT": 3}
    ai.baca_file_secrets = lambda: palsu

def test_halaman_login_terbuka():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file("app.py").run(timeout=30)
    assert not app.exception, app.exception
    assert app.title[0].value == "TIDE"


def test_semua_halaman_minta_login():
    import os
    from streamlit.testing.v1 import AppTest
    folder_pages = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
    for nama in sorted(os.listdir(folder_pages)):
        if nama.endswith(".py") and "tentang" not in nama.lower():
            app = AppTest.from_file("app.py").run(timeout=30)
            app.switch_page("pages/" + nama).run(timeout=30)
            assert not app.exception, (nama, app.exception)
            assert "login" in app.warning[0].value.lower(), nama


def test_bersihkan_jawaban():
    assert ai.bersihkan_jawaban("<think>mikir dulu</think>\nHalo!") == "Halo!"
    assert ai.bersihkan_jawaban("  Siap  ") == "Siap"


def test_pengaturan_dari_secrets():
    asli_file, asli_fungsi = ai.FILE_SECRETS, ai.baca_file_secrets
    path = tmp_file("secrets.toml")
    with open(path, "w", encoding="utf-8") as f:
        f.write('LOKAL_URL = "http://127.0.0.1:8888/v1"\nLOKAL_API_KEY = "sk-unsloth-abc"\n')
    try:
        ai.FILE_SECRETS = path
        ai.baca_file_secrets = asli_fungsi
        assert ai.baca_pengaturan("LOKAL_URL") == "http://127.0.0.1:8888/v1"
        assert ai.header_lokal() == {"Authorization": "Bearer sk-unsloth-abc"}
        assert ai.baca_pengaturan("LOKAL_MAKS_TOKEN") == 700              # tidak diisi -> nilai bawaan
    finally:
        ai.FILE_SECRETS = asli_file


def test_qwen_mati_memberi_pesan_jelas():
    matikan_ai()
    try:
        ai.panggil_qwen("halo")
        assert False, "seharusnya gagal"
    except ValueError as e:
        assert "Unsloth Studio" in str(e)
    assert ai.server_lokal_siap() is False


if __name__ == "__main__":
    print("Selesai. Gagal:", jalankan_tes(globals()))