import requests

URL_KOTA = "https://geocoding-api.open-meteo.com/v1/search"
URL_CUACA = "https://api.open-meteo.com/v1/forecast"

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
        raise ValueError("Gagal terhubung ke internet. Coba cek koneksi lalu coba lagi ya :)"))
    if resp.status_code != 200 :
        raise ValueError(f"Server data cuaca menolak permintaan (kode{resp.status_code}).") 
    try : 
        return resp.json()
    except ValueError :
        raise ValueError("Jawaban server data cuaca sulit dibaca we:(") 

def cari_lokasi (nama_kota) : 
    params = {"name" : nama_kota.strip(), "count" : 1, "language" : "id", "countryCode" : "ID"}
    hasil = minta_data(URL_KOTA, params).get("results") or []
    if not hasil : 
        raise ValueError(f"Kota '{nama_kota}' tidak ditemukan.")
    h = hasil[0]
    return {"nama": h.get("name", nama_kota), "provinsi" : h.get("admin1",""), "negara" : h.get("country", ""), 
            "label": h.get("name", nama_kota) + ", " + h.get("admin1", ""),
            "lat" : h["latitude"], "lon" : h["longitude"]}

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

def ambil_cuaca (lat, lon, tanggal) : 
    iso = tanggal.isoformat()
    params = {"latitude" : lat, "longitude":lon, "timezone":"auto", "start_date":iso, "end_date" : iso,
              "end_date" : iso, "hourly" : ("temperature_2m,apparent_temperature,relative_humidity_2m,precipitation_probability,"
                         "precipitation,weather_code,cloud_cover,wind_speed_10m,uv_index,is_day")}
    cuaca = minta_data(URL_CUACA, params)
    per_jam = olah_per_jam(cuaca["hourly"], {})
    harian = {"matahari_terbit": None, "matahari_terbenam": None}
    return per_jam, harian

def ambil_data(kota, tanggal, cache) : 
    lokasi = cari_lokasi(kota)
    per_jam, harian = ambil_cuaca(lokasi["lat"], lokasi["lon"], tanggal)
    return lokasi, per_jam, harian
