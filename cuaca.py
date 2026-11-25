import requests
from algoritma import quick_sort

URL_KOTA = "https://geocoding-api.open-meteo.com/v1/search"
URL_CUACA = "https://api.open-meteo.com/v1/forecast"
URL_UDARA = "https://air-quality-api.open-meteo.com/v1/air-quality"

KODE_CUACA = {
    0: "Cerah", 1: "Cerah berawan", 2: "Berawan sebagian", 3: "Mendung",
    45: "Berkabut", 48: "Berkabut",
    51: "Gerimis ringan", 53: "Gerimis", 55: "Gerimis lebat", 56: "Gerimis dingin", 57: "Gerimis dingin",
    61: "Hujan ringan", 63: "Hujan sedang", 65: "Hujan lebat", 66: "Hujan dingin", 67: "Hujan dingin",
    71: "Salju ringan", 73: "Salju", 75: "Salju lebat", 77: "Butiran salju",
    80: "Hujan lokal ringan", 81: "Hujan lokal", 82: "Hujan lokal lebat",
    85: "Hujan salju", 86: "Hujan salju lebat",
    95: "Badai petir", 96: "Badai petir dan hujan es", 99: "Badai petir dan hujan es"
}

def teks_kode(kode) : 
    if kode is None : 
        return "Tidak diketahui"
    return KODE_CUACA.get(int(kode), "Tidak diketahui")

def angka(nilai) : 
    if nilai is None : 
        return None
    return float(nilai)

def minta_data (url, params) : 
    try : 
        resp = requests.get(url, params=params, timeout=10)
    except requests.RequestException :
        raise ValueError("Gagal terhubung ke internet. Coba cek koneksi lalu coba lagi ya :)")
    if resp.status_code != 200 :
        raise ValueError(f"Server data cuaca menolak permintaan (kode{resp.status_code}).") 
    try : 
        return resp.json()
    except ValueError :
        raise ValueError("Jawaban server data cuaca sulit dibaca we:(") 

# def cari_lokasi (nama_kota) : 
#     params = {"name" : nama_kota.strip(), "count" : 1, "language" : "id", "countryCode" : "ID"}
#     hasil = minta_data(URL_KOTA, params).get("results") or []
#     if not hasil : 
#         raise ValueError(f"Kota '{nama_kota}' tidak ditemukan.")
#     h = hasil[0]
#     return {"nama": h.get("name", nama_kota), "provinsi" : h.get("admin1",""), "negara" : h.get("country", ""), 
#             "label": h.get("name", nama_kota) + ", " + h.get("admin1", ""),
#             "lat" : h["latitude"], "lon" : h["longitude"]}

def label_lokasi(hasil_api):
    bagian = [hasil_api.get("name", "")]
    for kunci in ["admin1", "country"]:
        if hasil_api.get(kunci) and hasil_api[kunci] not in bagian:
            bagian.append(hasil_api[kunci])
    return ", ".join(bagian)

def cocok_filter(hasil_api, filter_teks):
    tempat = " ".join([str(hasil_api.get(k, "")) for k in ["admin1", "admin2", "admin3", "country"]]).lower()
    for f in filter_teks:
        if f not in tempat:
            return False
    return True

BOBOT_TEMPAT = {"PPLC": 5, "PPLA": 4, "PPLA2": 3, "PPLA3": 2, "PPL": 1}

def nilai_prioritas(hasil_api, urutan):
    bobot = BOBOT_TEMPAT.get(hasil_api.get("feature_code", ""), 0)
    penduduk = hasil_api.get("population") or 0
    return bobot * 1e10 + penduduk - urutan * 0.001

def cari_lokasi(nama_kota) : 
    bagian = [b.strip() for b in nama_kota.split(",") if b.strip()]
    if not bagian:
        raise ValueError("Nama kota masih kosong.")
    nama = bagian[0]
    filter_teks = [b.lower() for b in bagian[1:]]

    daftar = []
    for kode_negara in ["ID", None]:  
        params = {"name": nama, "count": 10, "language": "id"}
        if kode_negara:
            params["countryCode"] = kode_negara
        hasil = minta_data(URL_KOTA, params).get("results") or []
        for i in range(len(hasil)):
            h = hasil[i]
            if cocok_filter(h, filter_teks):
                daftar.append({"nama": h.get("name", nama), "provinsi": h.get("admin1", ""),
                               "negara": h.get("country", ""), "label": label_lokasi(h),
                               "lat": h["latitude"], "lon": h["longitude"],
                               "prioritas": nilai_prioritas(h, i)})
        if daftar:
            break
    if not daftar:
        raise ValueError(f"Kota '{nama_kota}' tidak ditemukan. Coba ejaan lain atau tambahkan provinsi, "
                         "misalnya 'Pati, Jawa Tengah'.")
    return quick_sort(daftar, "prioritas")[0]


def olah_per_jam(jam, pm25) : 
    per_jam = []
    for i in range(len(jam["time"])) : 
        waktu = jam["time"][i]
        per_jam.append({
             "jam": int(waktu[11:13]),
            "kondisi": teks_kode(jam["weather_code"][i]),
            "suhu": angka(jam["temperature_2m"][i]),
            "terasa": angka(jam["apparent_temperature"][i]),
            "kelembapan": angka(jam["relative_humidity_2m"][i]),
            "hujan": angka(jam["precipitation_probability"][i]),
            "curah_mm": angka(jam["precipitation"][i]),
            "awan": angka(jam["cloud_cover"][i]),
            "angin": angka(jam["wind_speed_10m"][i]),
            "uv": angka(jam["uv_index"][i]),
            "siang": angka(jam["is_day"][i]),
            "pm25": angka(pm25.get(waktu)),
        })
    return per_jam

def ambil_p25(params) : 
    pm25 = {}
    try : 
        params_udara = dict(params)
        params_udara["hourly"] = "pm2_5"
        udara = minta_data(URL_UDARA, params_udara)
        waktu_list = udara["hourly"]["time"]
        nilai_list = udara["hourly"]["pm2_5"]
        for i in range(len(waktu_list)):
            pm25[waktu_list[i]] = nilai_list[i]
    except (ValueError, KeyError, TypeError):
        pm25 = {}
    return pm25


def ambil_cuaca (lat, lon, tanggal) : 
    iso = tanggal.isoformat()
    params = {"latitude" : lat, "longitude":lon, "timezone":"auto", "start_date":iso, "end_date" : iso}
    params_cuaca = dict(params)
    params_cuaca["hourly"] = ("temperature_2m,apparent_temperature,relative_humidity_2m,precipitation_probability," "precipitation,weather_code,cloud_cover,wind_speed_10m,uv_index,is_day")
    params_cuaca["daily"] = "sunrise,sunset"
    cuaca = minta_data(URL_CUACA, params_cuaca)
    jam = cuaca.get("hourly")
    
    if not jam or "time" not in jam or len(jam["time"]) < 24 : 
        raise ValueError ("Data cuaca untuk tanggal sekian belum tersedia")
    per_jam = olah_per_jam(jam, ambil_p25(params))
    harian = {"matahari_terbit": None, "matahari_terbenam": None}
    try:
        harian["matahari_terbit"] = cuaca["daily"]["sunrise"][0][11:16]
        harian["matahari_terbenam"] = cuaca["daily"]["sunset"][0][11:16]
    except (KeyError, IndexError, TypeError):
        pass
    return per_jam, harian
                     

def ambil_data(kota, tanggal, cache) :
    kunci = kota.strip().lower() + "|" + tanggal.isoformat()
    if kunci not in cache : 
        lokasi = cari_lokasi(kota)
        per_jam, harian = ambil_cuaca(lokasi["lat"], lokasi["lon"], tanggal)
        cache[kunci] = (lokasi, per_jam, harian)
    return cache[kunci]
