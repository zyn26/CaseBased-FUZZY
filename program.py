import pandas as pd

# =========================
# 1. BACA DATA EXCEL
# =========================
data = pd.read_excel("restoran.xlsx")


# =========================
# 2. FUNGSI KEANGGOTAAN
# =========================

# --- Pelayanan ---
def pelayanan_buruk(x):
    if x <= 40:
        return 1
    elif 40 < x < 60:
        return (60 - x) / (60 - 40)
    else:
        return 0

def pelayanan_sedang(x):
    if 40 <= x <= 60:
        return (x - 40) / (60 - 40)
    elif 60 < x <= 80:
        return (80 - x) / (80 - 60)
    else:
        return 0

def pelayanan_baik(x):
    if x <= 60:
        return 0
    elif 60 < x < 80:
        return (x - 60) / (80 - 60)
    else:
        return 1


# --- Harga ---
def harga_murah(x):
    if x <= 30000:
        return 1
    elif 30000 < x < 40000:
        return (40000 - x) / (40000 - 30000)
    else:
        return 0

def harga_sedang(x):
    if 30000 <= x <= 40000:
        return (x - 30000) / (40000 - 30000)
    elif 40000 < x <= 50000:
        return (50000 - x) / (50000 - 40000)
    else:
        return 0

def harga_mahal(x):
    if x <= 40000:
        return 0
    elif 40000 < x < 50000:
        return (x - 40000) / (50000 - 40000)
    else:
        return 1


# =========================
# 3. INFERENSI FUZZY
# =========================
def inferensi(pelayanan, harga):
    # fuzzifikasi pelayanan
    pb = pelayanan_buruk(pelayanan)
    ps = pelayanan_sedang(pelayanan)
    pg = pelayanan_baik(pelayanan)

    # fuzzifikasi harga
    hm = harga_murah(harga)
    hs = harga_sedang(harga)
    hh = harga_mahal(harga)

    rules = []

    # Rule 1
    rules.append((min(pg, hm), 100))

    # Rule 2
    rules.append((min(pg, hs), 90))

    # Rule 3
    rules.append((min(pg, hh), 70))

    # Rule 4
    rules.append((min(ps, hm), 80))

    # Rule 5
    rules.append((min(ps, hs), 60))

    # Rule 6
    rules.append((min(ps, hh), 40))

    # Rule 7
    rules.append((min(pb, hm), 50))

    # Rule 8
    rules.append((min(pb, hs), 30))

    # Rule 9
    rules.append((min(pb, hh), 10))

    return rules


# =========================
# 4. DEFUZZIFICATION
# =========================
def defuzzifikasi(rules):
    pembilang = 0
    penyebut = 0

    for alpha, nilai in rules:
        pembilang += alpha * nilai
        penyebut += alpha

    if penyebut == 0:
        return 0

    return pembilang / penyebut


# =========================
# 5. HITUNG SKOR SETIAP RESTORAN
# =========================
hasil = []

for index, row in data.iterrows():
    id_restoran = row["id Pelanggan"]
    pelayanan = row["Pelayanan"]
    harga = row["harga"]

    rules = inferensi(pelayanan, harga)
    skor = defuzzifikasi(rules)

    hasil.append([
        id_restoran,
        pelayanan,
        harga,
        skor
    ])


# =========================
# 6. SIMPAN KE DATAFRAME
# =========================
hasil_df = pd.DataFrame(
    hasil,
    columns=["ID Restoran", "Pelayanan", "Harga", "Skor"]
)

# urutkan skor tertinggi
hasil_df = hasil_df.sort_values(
    by="Skor",
    ascending=False
)

# ambil top 5
top5 = hasil_df.head(5)

print("===== TOP 5 RESTORAN TERBAIK =====")
print(top5)

# simpan ke excel
top5.to_excel("peringkat.xlsx", index=False)

print("\nFile peringkat.xlsx berhasil dibuat!")