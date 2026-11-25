from datetime import date

import akun
import cuaca
from bantuan_tes import contoh_hasil, harus_gagal, jalankan_tes, tmp_file


def json_cuaca_palsu():
    waktu = [f"2026-11-25T{j:02d}:00" for j in range(24)]
    return {"hourly": {"time": waktu,
                       "temperature_2m": [26.0] * 24, "apparent_temperature": [28.0] * 24,
                       "relative_humidity_2m": [70] * 24, "precipitation_probability": [10] * 24,
                       "precipitation": [0.0] * 24, "weather_code": [1] * 24, "cloud_cover": [40] * 24,
                       "wind_speed_10m": [7.5] * 24, "uv_index": [3.0] * 24, "is_day": [1] * 24},
            "daily": {"sunrise": ["2026-11-25T05:21"], "sunset": ["2026-11-25T17:48"]}}


def test_olah_per_jam():
    per_jam = cuaca.olah_per_jam(json_cuaca_palsu()["hourly"], {})
    assert len(per_jam) == 24
    assert per_jam[7]["jam"] == 7 and per_jam[7]["kondisi"] == "Cerah berawan"
    assert per_jam[7]["suhu"] == 26.0 and per_jam[7]["pm25"] is None
    assert cuaca.teks_kode(63) == "Hujan sedang" and cuaca.teks_kode(None) == "Tidak diketahui"


def test_login_register():
    path = tmp_file("users.json")
    assert akun.register("Valine", "rahasia1", "rahasia1", path) == "Valine"
    assert akun.muat_users(path) == {"Valine": "rahasia1"}
    harus_gagal(akun.register, "valine", "abcd", "abcd", path)            # nama sudah dipakai (huruf kecil)
    harus_gagal(akun.register, "Budi", "abcd", "abce", path)              # password ulang beda
    harus_gagal(akun.register, "Bu", "abcd", "abcd", path)                # nama terlalu pendek
    harus_gagal(akun.register, "Budi", "abc", "abc", path)                # password terlalu pendek
    assert akun.login(" valine ", "rahasia1", path) == "Valine"
    harus_gagal(akun.login, "Valine", "salah", path)
    harus_gagal(akun.login, "Tidak Ada", "abcd", path)
    assert akun.muat_users(path + ".tidak_ada") == {}


if __name__ == "__main__":
    print("Selesai. Gagal:", jalankan_tes(globals()))