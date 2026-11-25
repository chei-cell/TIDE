def quick_sort(data, kunci, menaik=False):
    if len(data) <= 1:                     
        return list(data)
    pivot = data[-1]
    kiri = []
    kanan = []
    for item in data[:-1]:
        if menaik:
            di_depan = item[kunci] < pivot[kunci]
        else:
            di_depan = item[kunci] > pivot[kunci]
        if di_depan:
            kiri.append(item)
        else:
            kanan.append(item)
    return quick_sort(kiri, kunci, menaik) + [pivot] + quick_sort(kanan, kunci, menaik)

def cari_rentang_kosong_terbaik(skor_slot, terisi, panjang):
    terbaik = None
    for awal in range(len(skor_slot) - panjang + 1):
        kosong = True
        for i in range(awal, awal + panjang):
            if terisi[i]:
                kosong = False
                break
        if not kosong:
            continue
        rata = sum(skor_slot[awal:awal + panjang]) / panjang
        if terbaik is None or rata > terbaik["rata2"]:
            terbaik = {"awal": awal, "rata2": rata}
    return terbaik

def cari_indeks(daftar, kunci, nilai):
    for i in range(len(daftar)):
        if daftar[i][kunci] == nilai:
            return i
    return -1