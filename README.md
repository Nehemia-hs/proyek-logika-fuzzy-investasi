# InvestRank — Sistem Rekomendasi Saham dengan Fuzzy-AHP

Sistem Pendukung Keputusan (SPK) berbasis web untuk meranking saham sektor **Consumer Goods** menggunakan metode **Fuzzy Analytical Hierarchy Process (Fuzzy-AHP)** dengan representasi **Triangular Fuzzy Number (TFN)** dan defuzzifikasi **Best Non-fuzzy Performance (BNP)**.

> Proyek Akhir — Mata Kuliah Logika Fuzzy (SCR)  
> Program Studi Teknik Informatika — Universitas Teknologi Yogyakarta, 2026

---

## Daftar Isi

1. [Cara Menjalankan](#cara-menjalankan)
2. [Struktur Proyek](#struktur-proyek)
3. [Saham yang Dianalisis](#saham-yang-dianalisis)
4. [Kriteria Penilaian](#kriteria-penilaian)
5. [Alur Perhitungan Fuzzy-AHP](#alur-perhitungan-fuzzy-ahp)
6. [Penjelasan Detail Matematis](#penjelasan-detail-matematis)
7. [Sumber Data Real-Time](#sumber-data-real-time)
8. [Cara Membaca Hasil](#cara-membaca-hasil)

---

## Cara Menjalankan

### Prasyarat

- Python **3.10** ke atas (proyek ini menggunakan Python 3.14)
- Koneksi internet (untuk mengambil data harga saham dari Yahoo Finance)

### Langkah 1 — Clone / Download Proyek

```bash
# Jika menggunakan git
git clone <url-repo> proyek_logikafuzzy_investrank
cd proyek_logikafuzzy_investrank

# Atau ekstrak ZIP, lalu masuk ke folder tersebut
cd proyek_logikafuzzy_investrank
```

### Langkah 2 — Buat Virtual Environment

```bash
python -m venv env
```

> Di Windows gunakan `python` atau `py`. Di macOS/Linux gunakan `python3`.

### Langkah 3 — Aktifkan Virtual Environment

| Sistem Operasi | Perintah |
|---|---|
| **Windows (CMD)** | `env\Scripts\activate` |
| **Windows (PowerShell)** | `env\Scripts\Activate.ps1` |
| **macOS / Linux** | `source env/bin/activate` |

Setelah berhasil, prompt terminal akan menampilkan `(env)` di awal baris.

### Langkah 4 — Install Dependensi

```bash
pip install -r requirements.txt
```

Dua paket yang diinstall:
- `flask` — framework web
- `yfinance` — pengambil data saham dari Yahoo Finance

### Langkah 5 — Jalankan Aplikasi

```bash
python app.py
```

Output yang muncul:

```
 * Running on http://127.0.0.1:5001
 * Debug mode: on
```

### Langkah 6 — Buka di Browser

Akses: **http://127.0.0.1:5001**

### Langkah 7 — Menghentikan Aplikasi

Tekan `Ctrl + C` di terminal.

### Menonaktifkan Virtual Environment (setelah selesai)

```bash
deactivate
```

---

## Struktur Proyek

```
proyek_logikafuzzy_investrank/
├── app.py              # Entry point Flask, routing utama
├── fuzzy_ahp.py        # Logika inti Fuzzy-AHP (TFN, BNP, CI/CR)
├── models.py           # Data saham, fetch real-time Yahoo Finance, ranking
├── history.py          # Simpan & muat riwayat analisis (riwayat.json)
├── requirements.txt    # Daftar dependensi Python
├── riwayat.json        # File penyimpanan riwayat analisis
├── templates/
│   └── dashboard.html  # Single-page dashboard (semua section)
└── static/
    └── assets/
        ├── css/
        │   └── style.css
        └── js/
            ├── dashboard.js   # Grafik tren harga saham (Chart.js)
            ├── saham.js       # Search & filter tabel saham
            ├── fuzzy_ahp.js   # Wizard input perbandingan berpasangan
            └── hasil.js       # Grafik bar ranking & donut bobot
```

---

## Saham yang Dianalisis

Lima saham sektor Consumer Goods Bursa Efek Indonesia (BEI):

| Kode | Perusahaan |
|------|-----------|
| **UNVR** | Unilever Indonesia Tbk |
| **ICBP** | Indofood CBP Sukses Makmur Tbk |
| **KLBF** | Kalbe Farma Tbk |
| **MYOR** | Mayora Indah Tbk |
| **HMSP** | HM Sampoerna Tbk |

Data harga dan historis diambil secara real-time dari **Yahoo Finance** (ticker `.JK`). Jika koneksi gagal, sistem menggunakan data fallback statis.

---

## Kriteria Penilaian

Sistem menggunakan **4 kriteria** penilaian saham:

| Kriteria | Jenis | Keterangan |
|----------|-------|-----------|
| **Return** | Benefit ↑ | Return bulanan ternormalisasi. Semakin tinggi semakin baik. |
| **Risiko** | Cost ↓ | Volatilitas harga (standar deviasi return harian). Semakin rendah semakin baik. |
| **Dividend Yield** | Benefit ↑ | Persentase dividen terhadap harga. Semakin tinggi semakin baik. |
| **Stabilitas** | Benefit ↑ | Kestabilan harga `1 - (max-min)/max`. Semakin stabil semakin baik. |

**Benefit Criteria**: nilai lebih tinggi = lebih baik.  
**Cost Criteria**: nilai lebih rendah = lebih baik (dalam skor akhir, risiko dibalik: `1 - risiko`).

Semua nilai kriteria dinormalisasi ke rentang **0–1** menggunakan min-max normalization.

---

## Alur Perhitungan Fuzzy-AHP

```
Input User (6 slider)
        │
        ▼
┌──────────────────────────────────┐
│  1. Konversi Slider → Saaty      │
│     slider 5    → Saaty 1        │
│     slider 6/4  → Saaty 3        │
│     slider 7/3  → Saaty 5        │
│     slider 8/2  → Saaty 7        │
│     slider 9/1  → Saaty 9        │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  2. Konversi Saaty → TFN         │
│     1 → (1, 1, 1)                │
│     3 → (2, 3, 4)                │
│     5 → (4, 5, 6)                │
│     7 → (6, 7, 8)                │
│     9 → (8, 9, 9)                │
│     Resiprokal: (l,m,u)⁻¹        │
│              = (1/u, 1/m, 1/l)   │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  3. Bangun Matriks TFN 4×4       │
│     Diagonal = (1, 1, 1)         │
│     a[i][j] = TFN jika i lebih   │
│     penting, resiprokalnya di    │
│     a[j][i]                      │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  4. Hitung Bobot Fuzzy           │
│     Geometric mean per baris →   │
│     normalisasi → TFN bobot      │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  5. Defuzzifikasi BNP            │
│     BNP = (l + m + u) / 3        │
│     → bobot crisp (ternormalisasi│
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  6. Uji Konsistensi (CI/CR)      │
│     λ_max → CI = (λ-n)/(n-1)     │
│     CR = CI / RI  (RI=0.90, n=4) │
│     CR ≤ 0.10 = konsisten        │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  7. Hitung Skor Saham            │
│  S = w_r·R + w_ri·(1-Ri)         │
│    + w_d·D + w_s·St              │
└──────────────┬───────────────────┘
               │
               ▼
         Ranking Saham
```

---

## Penjelasan Detail Matematis

### Langkah 1 — Input Perbandingan Berpasangan

User membandingkan **6 pasangan** dari 4 kriteria menggunakan **slider 1–9**:

| Pasangan | Keterangan |
|----------|-----------|
| Risiko vs Return | Langsung (step 1) |
| Dividend vs Risiko | Langsung (step 2) |
| Stabilitas vs Dividend | Langsung (step 3) |
| Dividend vs Return | Turunan (otomatis dari step 1×2) |
| Stabilitas vs Return | Turunan (otomatis dari step 1×2×3) |
| Stabilitas vs Risiko | Turunan (otomatis dari step 2×3) |

Slider tengah (5) = **sama penting**. Sisi kiri = kriteria kiri lebih penting. Sisi kanan = kriteria kanan lebih penting.

Formula konversi slider ke skala Saaty:
```
Saaty = 1 + 2 × |slider - 5|
```

### Langkah 2 — Konversi ke Triangular Fuzzy Number (TFN)

TFN merepresentasikan **ketidakpastian penilaian manusia**. Setiap nilai Saaty diubah ke triplet `(l, m, u)`:

| Saaty | Definisi | TFN (l, m, u) | Resiprokal |
|-------|----------|---------------|-----------|
| 1 | Sama penting | (1, 1, 1) | (1.000, 1.000, 1.000) |
| 3 | Sedikit lebih penting | (2, 3, 4) | (0.250, 0.333, 0.500) |
| 5 | Lebih penting | (4, 5, 6) | (0.167, 0.200, 0.250) |
| 7 | Sangat lebih penting | (6, 7, 8) | (0.125, 0.143, 0.167) |
| 9 | Mutlak lebih penting | (8, 9, 9) | (0.111, 0.111, 0.125) |

Resiprokal TFN: `(l, m, u)⁻¹ = (1/u, 1/m, 1/l)`

### Langkah 3 — Matriks Perbandingan TFN (4×4)

Matriks `A` berukuran 4×4 dibangun dengan:
- Diagonal: `(1, 1, 1)` (setiap kriteria sama penting dengan dirinya sendiri)
- `a[i][j]` = TFN jika kriteria `i` lebih penting dari `j`
- `a[j][i]` = resiprokal dari `a[i][j]`

### Langkah 4 — Bobot Fuzzy via Geometric Mean

Untuk setiap baris `i`, hitung **geometric mean** dari seluruh elemen TFN pada baris tersebut:

```
r̃ᵢ = (ã_{i1} ⊗ ã_{i2} ⊗ ... ⊗ ã_{in})^(1/n)
```

Dengan notasi komponen:
```
l_gm = (∏ aᵢⱼ.l)^(1/n)
m_gm = (∏ aᵢⱼ.m)^(1/n)
u_gm = (∏ aᵢⱼ.u)^(1/n)
```

Kemudian normalisasi (pembagi dibalik komponen untuk mempertahankan sifat TFN):
```
wᵢ.l = l_gmᵢ / Σ(u_gmⱼ)
wᵢ.m = m_gmᵢ / Σ(m_gmⱼ)
wᵢ.u = u_gmᵢ / Σ(l_gmⱼ)
```

### Langkah 5 — Defuzzifikasi BNP

Konversi TFN bobot ke nilai crisp menggunakan metode **Best Non-fuzzy Performance**:

```
BNPᵢ = (lᵢ + mᵢ + uᵢ) / 3
```

Bobot akhir dinormalisasi agar jumlahnya = 1:
```
wᵢ = BNPᵢ / Σ BNPⱼ
```

### Langkah 6 — Uji Konsistensi (CI & CR)

Konsistensi dihitung dari bobot crisp terhadap matriks nilai tengah `m`:

```
Weighted Sum Vectorᵢ = Σⱼ (a[i][j].m × wⱼ)

λ_max = (1/n) × Σ (WSVᵢ / wᵢ)

CI = (λ_max - n) / (n - 1)

CR = CI / RI
```

Untuk **n = 4**: `RI = 0.90` (Random Index tabel Saaty)

| CR | Status |
|----|--------|
| ≤ 0.10 | ✅ Konsisten — hasil dapat dipercaya |
| > 0.10 | ⚠️ Tidak konsisten — disarankan ulangi input |

### Langkah 7 — Skor Akhir Saham

Setiap saham dihitung skornya dengan **weighted sum**:

```
Skor = w_return   × R
     + w_risiko   × (1 − Ri)   ← risiko dibalik (cost criterion)
     + w_dividend × D
     + w_stabilitas × St
```

| Variabel | Arti |
|----------|------|
| `R` | Nilai return ternormalisasi (0–1) |
| `Ri` | Nilai risiko ternormalisasi (0–1); dibalik karena cost criterion |
| `D` | Nilai dividend yield ternormalisasi (0–1) |
| `St` | Nilai stabilitas ternormalisasi (0–1) |

Saham dengan **skor tertinggi** adalah rekomendasi utama.

---

## Sumber Data Real-Time

Data diambil otomatis dari **Yahoo Finance** via library `yfinance`:

- **Periode historis**: 30 hari terakhir (interval harian)
- **Data yang diambil**: harga penutupan, dividend yield
- **Cache**: data disimpan selama **5 menit** agar tidak terlalu sering fetch
- **Fallback**: jika Yahoo Finance tidak tersedia, sistem menggunakan data statis bawaan

Tombol **Refresh** di halaman utama akan mengosongkan cache dan mengambil data terbaru.

---

## Cara Membaca Hasil

### Skor Saham

| Skor | Kategori |
|------|---------|
| ≥ 0.75 | 🟢 Sangat Direkomendasikan |
| 0.60 – 0.74 | 🟡 Layak Dipertimbangkan |
| < 0.60 | 🔵 Stabil |

### Bobot Kriteria

Bobot menunjukkan **seberapa besar pengaruh** setiap kriteria dalam keputusan akhir. Jumlah semua bobot = **1.00 (100%)**.

Contoh: bobot Return = 0.43 artinya 43% dari skor saham ditentukan oleh kriteria Return.

### Interpretasi CR

- **CR = 0.00**: perbandingan sempurna konsisten (biasanya saat semua slider di tengah)
- **CR < 0.10**: konsisten, hasil dapat digunakan
- **CR > 0.10**: perbandingan bertentangan satu sama lain; disarankan kembali dan revisi input

---

## Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|----------|
| Backend | Python 3, Flask |
| Metode SPK | Fuzzy-AHP (TFN + BNP) |
| Data Saham | Yahoo Finance (`yfinance`) |
| Grafik | Chart.js |
| Ikon | Font Awesome 6 |
| Font | Google Fonts — Poppins |
