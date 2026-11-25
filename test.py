import importlib
import os

from bantuan_tes import jalankan_tes

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_TES = ["test_jadwal", "test_data", "test_tampilan"] 

total_gagal = 0
for nama in FILE_TES:
    if not os.path.exists(os.path.join(FOLDER, nama + ".py")):
        print(f"--- {nama}.py belum ada, dilewati")
        continue
    print(f"--- {nama}.py")
    modul = importlib.import_module(nama)
    total_gagal += jalankan_tes(vars(modul))
print("Selesai. Gagal:", total_gagal)
