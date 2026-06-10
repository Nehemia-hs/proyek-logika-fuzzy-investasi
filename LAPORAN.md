# LAPORAN PROYEK AKHIR

## SISTEM REKOMENDASI SAHAM CONSUMER GOODS MENGGUNAKAN METODE FUZZY ANALYTICAL HIERARCHY PROCESS (FUZZY-AHP)

---

|  |  |
|--|--|
| **Nama Sistem** | InvestRank |
| **Mata Kuliah** | Logika Fuzzy (SCR) |
| **Program Studi** | Teknik Informatika |
| **Universitas** | Universitas Teknologi Yogyakarta |
| **Tahun** | 2026 |

---

## DAFTAR ISI

1. [Pendahuluan](#bab-i-pendahuluan)
   - 1.1 Latar Belakang
   - 1.2 Rumusan Masalah
   - 1.3 Tujuan
   - 1.4 Manfaat
   - 1.5 Batasan Masalah
2. [Landasan Teori](#bab-ii-landasan-teori)
   - 2.1 Sistem Pendukung Keputusan
   - 2.2 Saham Sektor Consumer Goods
   - 2.3 Analytical Hierarchy Process (AHP)
   - 2.4 Triangular Fuzzy Number (TFN)
   - 2.5 Fuzzy-AHP
   - 2.6 Defuzzifikasi BNP
   - 2.7 Uji Konsistensi
3. [Metodologi](#bab-iii-metodologi)
   - 3.1 Alur Penelitian
   - 3.2 Kriteria Penilaian
   - 3.3 Alternatif (Saham)
   - 3.4 Normalisasi Data
   - 3.5 Arsitektur Sistem
4. [Implementasi dan Pembahasan](#bab-iv-implementasi-dan-pembahasan)
   - 4.1 Tampilan Sistem
   - 4.2 Contoh Perhitungan Lengkap
   - 4.3 Hasil Ranking
   - 4.4 Analisis Pengaruh Bobot
5. [Kesimpulan dan Saran](#bab-v-kesimpulan-dan-saran)
6. [Daftar Pustaka](#daftar-pustaka)

---

## BAB I PENDAHULUAN

### 1.1 Latar Belakang

Investasi saham merupakan salah satu instrumen keuangan yang diminati masyarakat untuk mengembangkan aset. Namun, pemilihan saham yang tepat bukan perkara mudah karena melibatkan banyak kriteria yang saling berkaitan, seperti tingkat keuntungan (*return*), risiko volatilitas, pembagian dividen, dan stabilitas harga. Investor pemula seringkali kesulitan mengintegrasikan seluruh faktor tersebut secara rasional dan terukur.

Sektor **Consumer Goods** (Barang Konsumsi) merupakan salah satu sektor yang relatif defensif di Bursa Efek Indonesia (BEI). Saham-saham sektor ini cenderung stabil karena produknya selalu dibutuhkan masyarakat terlepas dari kondisi ekonomi. Namun, performa antar emiten tetap bervariasi, sehingga diperlukan alat bantu pengambilan keputusan yang mampu membandingkan saham-saham tersebut secara objektif.

Metode **Analytical Hierarchy Process (AHP)** yang dikembangkan oleh Thomas L. Saaty (1980) merupakan metode Sistem Pendukung Keputusan (SPK) yang populer untuk masalah multi-kriteria. Namun, AHP konvensional tidak dapat mengakomodasi ketidakpastian (*uncertainty*) dalam penilaian manusia. Seorang investor yang menyatakan "Return sedikit lebih penting dari Risiko" sesungguhnya mengandung ambiguitas yang tidak dapat direpresentasikan oleh satu angka bulat.

**Fuzzy-AHP** hadir sebagai solusi dengan mengintegrasikan logika fuzzy ke dalam proses AHP. Penilaian perbandingan tidak lagi berupa angka tunggal, melainkan **Triangular Fuzzy Number (TFN)** yang merepresentasikan rentang kemungkinan nilai, sehingga ketidakpastian penilaian manusia dapat ditangkap secara matematis.

Berdasarkan latar belakang tersebut, dibangunlah sistem **InvestRank**: sebuah aplikasi web berbasis Python/Flask yang membantu investor menentukan rekomendasi saham Consumer Goods menggunakan metode Fuzzy-AHP dengan defuzzifikasi **Best Non-fuzzy Performance (BNP)**.

### 1.2 Rumusan Masalah

1. Bagaimana membangun sistem yang dapat membantu investor menentukan prioritas kriteria investasi saham secara interaktif?
2. Bagaimana menerapkan metode Fuzzy-AHP dengan TFN untuk mengolah penilaian perbandingan berpasangan yang mengandung ketidakpastian?
3. Bagaimana mengintegrasikan data harga saham real-time ke dalam proses perankingan?

### 1.3 Tujuan

1. Merancang dan mengimplementasikan sistem rekomendasi saham Consumer Goods berbasis web.
2. Menerapkan metode Fuzzy-AHP dengan representasi TFN dan defuzzifikasi BNP untuk menghitung bobot kriteria.
3. Mengintegrasikan data real-time dari Yahoo Finance sebagai nilai alternatif saham.
4. Menghasilkan ranking saham yang dapat digunakan sebagai referensi keputusan investasi.

### 1.4 Manfaat

- **Bagi Investor Pemula**: Mendapatkan rekomendasi saham berbasis data dan metode ilmiah tanpa perlu memahami seluruh matematika di baliknya.
- **Bagi Akademisi**: Sebagai contoh implementasi nyata logika fuzzy dalam masalah pengambilan keputusan finansial.
- **Bagi Pengembangan Ilmu**: Menunjukkan keunggulan Fuzzy-AHP dibandingkan AHP konvensional dalam menangani ketidakpastian penilaian.

### 1.5 Batasan Masalah

1. Saham yang dianalisis dibatasi pada **5 emiten** sektor Consumer Goods: UNVR, ICBP, KLBF, MYOR, dan HMSP.
2. Kriteria penilaian dibatasi pada **4 kriteria**: Return, Risiko, Dividend Yield, dan Stabilitas.
3. Data real-time diambil dari Yahoo Finance dengan periode historis **30 hari terakhir**.
4. Metode defuzzifikasi yang digunakan adalah **BNP (Best Non-fuzzy Performance)**.
5. Sistem berjalan sebagai aplikasi web lokal (*localhost*), bukan cloud/server publik.

---

## BAB II LANDASAN TEORI

### 2.1 Sistem Pendukung Keputusan (SPK)

Sistem Pendukung Keputusan (*Decision Support System*/DSS) adalah sistem berbasis komputer yang membantu pengambil keputusan dalam menghadapi masalah semi-terstruktur dengan cara mengolah data dan model analitis. SPK tidak menggantikan keputusan manusia, melainkan menyediakan informasi dan analisis yang memperkuat kualitas keputusan.

Komponen utama SPK:
- **Database**: penyimpanan data yang relevan
- **Model Base**: kumpulan model matematis/analitis
- **User Interface**: antarmuka interaksi pengguna

### 2.2 Saham Sektor Consumer Goods

Saham sektor Consumer Goods termasuk dalam klasifikasi **IDX Consumer Non-Cyclicals** di Bursa Efek Indonesia. Karakteristik utama sektor ini:

- Produk yang dijual merupakan kebutuhan sehari-hari (makanan, minuman, produk rumah tangga, farmasi)
- Permintaan relatif stabil meskipun terjadi resesi ekonomi (*defensive stock*)
- Umumnya membayar dividen secara rutin
- Volatilitas harga lebih rendah dibandingkan sektor siklikal

Lima emiten yang dianalisis dalam sistem ini:

| Kode | Perusahaan | Produk Utama |
|------|-----------|-------------|
| UNVR | Unilever Indonesia Tbk | Sabun, sampo, es krim, teh |
| ICBP | Indofood CBP Sukses Makmur Tbk | Mi instan, minuman, bumbu |
| KLBF | Kalbe Farma Tbk | Obat-obatan, nutrisi, distribusi |
| MYOR | Mayora Indah Tbk | Biskuit, kopi, permen, wafer |
| HMSP | HM Sampoerna Tbk | Rokok dan produk tembakau |

### 2.3 Analytical Hierarchy Process (AHP)

AHP dikembangkan oleh **Thomas L. Saaty** pada tahun 1980. Metode ini mendekomposisi masalah kompleks menjadi hierarki: **Tujuan → Kriteria → Alternatif**.

**Skala Saaty** digunakan untuk perbandingan berpasangan:

| Nilai | Keterangan |
|-------|-----------|
| 1 | Sama penting |
| 3 | Sedikit lebih penting |
| 5 | Lebih penting |
| 7 | Sangat lebih penting |
| 9 | Mutlak lebih penting |
| 2, 4, 6, 8 | Nilai tengah antara dua penilaian berdekatan |

Matriks perbandingan berpasangan `A` bersifat **resiprokal**: jika `a[i][j] = x`, maka `a[j][i] = 1/x`.

**Kelemahan AHP konvensional**: penilaian manusia bersifat subjektif dan mengandung ketidakpastian yang tidak dapat direpresentasikan oleh satu angka pasti.

### 2.4 Triangular Fuzzy Number (TFN)

TFN adalah bilangan fuzzy yang didefinisikan oleh tiga parameter `(l, m, u)`:
- `l` (*lower*): batas bawah — nilai terendah yang mungkin
- `m` (*middle*): nilai paling representatif (modus)
- `u` (*upper*): batas atas — nilai tertinggi yang mungkin

Dengan syarat: `l ≤ m ≤ u`

**Fungsi keanggotaan TFN**:

```
         0          , x < l
         (x-l)/(m-l), l ≤ x ≤ m
μ(x) =  (u-x)/(u-m), m < x ≤ u
         0          , x > u
```

**Operasi pada TFN**:
- Penjumlahan: `(l₁,m₁,u₁) + (l₂,m₂,u₂) = (l₁+l₂, m₁+m₂, u₁+u₂)`
- Perkalian: `(l₁,m₁,u₁) × (l₂,m₂,u₂) ≈ (l₁×l₂, m₁×m₂, u₁×u₂)`
- Resiprokal: `(l,m,u)⁻¹ = (1/u, 1/m, 1/l)`

**Tabel konversi Saaty → TFN** yang digunakan:

| Saaty | TFN (l, m, u) | TFN Resiprokal |
|-------|--------------|----------------|
| 1 | (1, 1, 1) | (1.000, 1.000, 1.000) |
| 3 | (2, 3, 4) | (0.250, 0.333, 0.500) |
| 5 | (4, 5, 6) | (0.167, 0.200, 0.250) |
| 7 | (6, 7, 8) | (0.125, 0.143, 0.167) |
| 9 | (8, 9, 9) | (0.111, 0.111, 0.125) |

### 2.5 Fuzzy-AHP

Fuzzy-AHP (Chang, 1996; Buckley, 1985) menggabungkan kelebihan AHP dalam menstrukturkan masalah hierarki dengan kemampuan logika fuzzy dalam menangani ketidakpastian.

**Perbedaan AHP vs Fuzzy-AHP**:

| Aspek | AHP Konvensional | Fuzzy-AHP |
|-------|-----------------|----------|
| Input perbandingan | Angka bulat (1–9) | TFN (l, m, u) |
| Representasi ketidakpastian | Tidak ada | Rentang nilai [l, u] |
| Bobot kriteria | Nilai tunggal | TFN → perlu defuzzifikasi |
| Kesesuaian penilaian manusia | Terbatas | Lebih realistis |

**Metode geometric mean (Buckley, 1985)** digunakan untuk menghitung bobot fuzzy:

```
r̃ᵢ = (ã_{i1} ⊗ ã_{i2} ⊗ ... ⊗ ã_{in})^(1/n)
```

di mana `⊗` adalah operasi perkalian TFN.

### 2.6 Defuzzifikasi BNP

**Best Non-fuzzy Performance (BNP)** adalah metode defuzzifikasi yang mengkonversi TFN ke satu nilai crisp menggunakan rata-rata ketiga parameter:

```
BNP = (l + m + u) / 3
```

BNP dipilih karena:
- Komputasi sederhana dan efisien
- Mempertimbangkan ketiga batas (bawah, tengah, atas) secara seimbang
- Cocok untuk kondisi di mana tidak ada preferensi terhadap nilai optimis/pesimis

### 2.7 Uji Konsistensi

Konsistensi logis penilaian diuji melalui **Consistency Ratio (CR)**.

Dalam Fuzzy-AHP, uji konsistensi secara penuh menggunakan TFN sangat kompleks. Oleh karena itu, pendekatan yang lazim digunakan dalam literatur (dan diterapkan dalam sistem ini) adalah **aproksimasi menggunakan nilai tengah matriks TFN** dan **bobot crisp hasil BNP**:

```
WSVᵢ = Σⱼ (a[i][j].m × wⱼ)   ← menggunakan nilai m (modus) TFN
                                   dan bobot crisp hasil defuzzifikasi

λ_max = (1/n) × Σ (WSVᵢ / wᵢ)
CI    = (λ_max - n) / (n - 1)
CR    = CI / RI
```

Pendekatan ini dikenal sebagai *defuzzified consistency check* dan diterima secara luas dalam penelitian Fuzzy-AHP (Buckley, 1985; Kahraman et al., 2004) karena menghitung konsistensi dari matriks nilai tengah TFN setara dengan menguji apakah **preferensi inti (mode)** pengambil keputusan sudah logis dan tidak saling bertentangan.

**Random Index (RI)** untuk berbagai ukuran matriks (Saaty, 1980):

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| RI | 0.00 | 0.00 | 0.58 | **0.90** | 1.12 | 1.24 | 1.32 |

Penilaian dianggap **konsisten** jika `CR ≤ 0.10`.

---

## BAB III METODOLOGI

### 3.1 Alur Penelitian

```
┌────────────────────────────────────────────────────────────────┐
│                       ALUR SISTEM                              │
│                                                                │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ Data Saham  │    │  Input User  │    │   Fuzzy-AHP      │  │
│  │ (Yahoo      │    │  (6 slider   │    │  ┌────────────┐  │  │
│  │  Finance /  │    │   perband.   │    │  │ Slider →   │  │  │
│  │  Fallback)  │    │   berpasang) │    │  │ Saaty → TFN│  │  │
│  └──────┬──────┘    └──────┬───────┘    │  ├────────────┤  │  │
│         │                  │            │  │ Matriks    │  │  │
│         ▼                  ▼            │  │ TFN 4×4    │  │  │
│  ┌─────────────────────────────────┐   │  ├────────────┤  │  │
│  │   Normalisasi Min-Max (0–1)     │   │  │ Geo. Mean  │  │  │
│  │   Return, Risiko, Dividend,     │──▶│  │ + BNP      │  │  │
│  │   Stabilitas per saham          │   │  ├────────────┤  │  │
│  └─────────────────────────────────┘   │  │ CI / CR    │  │  │
│                                        │  │ uji kons.  │  │  │
│                                        │  └────────────┘  │  │
│                                        └────────┬─────────┘  │
│                                                 │             │
│                                                 ▼             │
│                              ┌──────────────────────────────┐ │
│                              │  Skor Saham (Weighted Sum)   │ │
│                              │  S = wr·R + wri·(1−Ri)       │ │
│                              │    + wd·D + ws·St            │ │
│                              └──────────────┬───────────────┘ │
│                                             │                  │
│                                             ▼                  │
│                                    ┌─────────────────┐        │
│                                    │  Ranking Saham  │        │
│                                    └─────────────────┘        │
└────────────────────────────────────────────────────────────────┘
```

### 3.2 Kriteria Penilaian

Empat kriteria yang digunakan beserta metode perhitungannya:

| No | Kriteria | Jenis | Rumus / Sumber | Keterangan |
|----|----------|-------|----------------|-----------|
| C1 | **Return** | Benefit ↑ | `(harga_akhir / harga_awal - 1) × 100%` | Return bulanan dari data historis |
| C2 | **Risiko** | Cost ↓ | Standar deviasi return harian | Semakin kecil semakin aman |
| C3 | **Dividend Yield** | Benefit ↑ | `dividen_per_saham / harga_saham` | Dari data Yahoo Finance atau fallback statis |
| C4 | **Stabilitas** | Benefit ↑ | `1 - (harga_max - harga_min) / harga_max` | Mendekati 1 = harga sangat stabil |

**Penanganan Cost Criterion (Risiko)**: Karena risiko bersifat *cost* (semakin kecil semakin baik), dalam perhitungan skor akhir nilai risiko dibalik menjadi `(1 − risiko_ternormalisasi)` sehingga saham berisiko rendah mendapat skor tinggi.

### 3.3 Alternatif (Saham)

| No | Kode | Nama Lengkap |
|----|------|-------------|
| A1 | UNVR | PT Unilever Indonesia Tbk |
| A2 | ICBP | PT Indofood CBP Sukses Makmur Tbk |
| A3 | KLBF | PT Kalbe Farma Tbk |
| A4 | MYOR | PT Mayora Indah Tbk |
| A5 | HMSP | PT HM Sampoerna Tbk |

### 3.4 Normalisasi Data

Semua nilai kriteria dinormalisasi ke rentang [0, 1] menggunakan **min-max normalization**:

```
x_norm = (x - x_min) / (x_max - x_min)
```

Jika `x_max = x_min` (semua saham bernilai sama), maka semua saham mendapat nilai 0.5.

### 3.5 Arsitektur Sistem

Sistem dibangun dengan arsitektur **MVC (Model–View–Controller)** berbasis web:

```
┌──────────────────────────────────────────────────────┐
│                    Browser (Client)                  │
│   dashboard.html + style.css                         │
│   dashboard.js | saham.js | fuzzy_ahp.js | hasil.js  │
└──────────────────────┬───────────────────────────────┘
                       │  HTTP (Flask Routes)
┌──────────────────────▼───────────────────────────────┐
│                    app.py (Controller)               │
│  /dashboard  /ahp/submit  /riwayat/*  /api/*         │
└──────┬──────────────────────────┬────────────────────┘
       │                          │
┌──────▼──────┐          ┌────────▼───────┐
│ fuzzy_ahp.py│          │   models.py    │
│ (Fuzzy-AHP  │          │ (Data Saham +  │
│  Engine)    │          │  Yahoo Finance │
└─────────────┘          │  + Ranking)    │
                         └────────┬───────┘
                                  │
                         ┌────────▼───────┐
                         │  history.py    │
                         │ (riwayat.json) │
                         └────────────────┘
```

---

## BAB IV IMPLEMENTASI DAN PEMBAHASAN

### 4.1 Tampilan Sistem

Sistem InvestRank menggunakan desain *single-page* dengan navigasi antar section:

| Section | Isi |
|---------|-----|
| **Dashboard** | Hero section, grafik tren harga 30 hari, statistik ringkas |
| **Data Saham** | Tabel lengkap data 5 saham dengan filter dan search |
| **Kriteria** | Penjelasan 4 kriteria penilaian |
| **Metodologi** | Alur Fuzzy-AHP, tabel TFN, rumus matematis |
| **Fuzzy AHP** | Wizard 6 langkah input perbandingan berpasangan + riwayat analisis |
| **Hasil** | Ranking, grafik bar skor, donut bobot, matriks TFN |

**Fitur wizard Fuzzy-AHP**:
- Slider 1–9 dengan label kiri/kanan yang jelas
- Preview pilihan real-time (text + kekuatan preferensi)
- 3 perbandingan langsung → 3 turunan dihitung otomatis (saran konsisten)
- Tabel ringkasan sebelum submit

### 4.2 Contoh Perhitungan Lengkap

Berikut adalah contoh perhitungan dari sesi analisis yang telah dilakukan pada sistem, dengan input sebagai berikut:

**Input Perbandingan Berpasangan:**

| No | Pasangan Kriteria | Nilai Slider | Saaty | Arah |
|----|------------------|-------------|-------|------|
| 1 | Return vs Risiko | 7 | 5 | Return lebih penting |
| 2 | Risiko vs Dividend | 5 | 1 | Sama penting |
| 3 | Dividend vs Stabilitas | 8 | 7 | Dividend lebih penting |
| 4 | Return vs Dividend | 5* | 1 | Sama penting (turunan) |
| 5 | Return vs Stabilitas | 8* | 7 | Return lebih penting (turunan) |
| 6 | Risiko vs Stabilitas | 8* | 7 | Risiko lebih penting (turunan) |

*) Dihitung otomatis dari perbandingan langsung

---

#### Langkah 1 — Konversi ke Skala Saaty

Formula: `Saaty = 1 + 2 × |slider − 5|`

- Slider 7 → Saaty = 1 + 2 × |7−5| = 1 + 4 = **5**
- Slider 5 → Saaty = 1 (sama penting)
- Slider 8 → Saaty = 1 + 2 × |8−5| = 1 + 6 = **7**

---

#### Langkah 2 — Konversi ke TFN

| Pasangan | Saaty | TFN a[i][j] | TFN a[j][i] (Resiprokal) |
|----------|-------|-------------|--------------------------|
| Return vs Risiko (a[0][1]) | 5 → Return penting | **(4, 5, 6)** | (0.167, 0.200, 0.250) |
| Return vs Dividend (a[0][2]) | 1 → Sama | **(1, 1, 1)** | (1, 1, 1) |
| Return vs Stabilitas (a[0][3]) | 7 → Return penting | **(6, 7, 8)** | (0.125, 0.143, 0.167) |
| Risiko vs Dividend (a[1][2]) | 1 → Sama | **(1, 1, 1)** | (1, 1, 1) |
| Risiko vs Stabilitas (a[1][3]) | 7 → Risiko penting | **(6, 7, 8)** | (0.125, 0.143, 0.167) |
| Dividend vs Stabilitas (a[2][3]) | 7 → Dividend penting | **(6, 7, 8)** | (0.125, 0.143, 0.167) |

---

#### Langkah 3 — Matriks Perbandingan TFN (4×4)

Baris = Return, Risiko, Dividend, Stabilitas:

|  | **Return** | **Risiko** | **Dividend** | **Stabilitas** |
|--|-----------|-----------|-------------|---------------|
| **Return** | (1, 1, 1) | (4, 5, 6) | (1, 1, 1) | (6, 7, 8) |
| **Risiko** | (0.167, 0.200, 0.250) | (1, 1, 1) | (0.167, 0.200, 0.250) | (1, 1, 1) |
| **Dividend** | (1, 1, 1) | (4, 5, 6) | (1, 1, 1) | (6, 7, 8) |
| **Stabilitas** | (0.125, 0.143, 0.167) | (1, 1, 1) | (0.125, 0.143, 0.167) | (1, 1, 1) |

---

#### Langkah 4 — Geometric Mean per Baris

**Baris Return** `(1,1,1), (4,5,6), (1,1,1), (6,7,8)` — n = 4:

```
l_gm = (1 × 4 × 1 × 6)^(1/4) = (24)^0.25 = 2.2134
m_gm = (1 × 5 × 1 × 7)^(1/4) = (35)^0.25 = 2.4323
u_gm = (1 × 6 × 1 × 8)^(1/4) = (48)^0.25 = 2.6318
```

**Baris Risiko** `(0.167,0.2,0.25), (1,1,1), (0.167,0.2,0.25), (1,1,1)`:

```
l_gm = (0.167 × 1 × 0.167 × 1)^0.25 = (0.0279)^0.25 = 0.4082
m_gm = (0.2   × 1 × 0.2   × 1)^0.25 = (0.0400)^0.25 = 0.4472
u_gm = (0.25  × 1 × 0.25  × 1)^0.25 = (0.0625)^0.25 = 0.5000
```

**Baris Dividend** (sama dengan baris Return karena penilaian identik):

```
l_gm = 2.2134,  m_gm = 2.4323,  u_gm = 2.6318
```

**Baris Stabilitas** `(0.125,0.143,0.167), (1,1,1), (0.125,0.143,0.167), (1,1,1)`:

```
l_gm = (0.125 × 1 × 0.125 × 1)^0.25 = (0.01563)^0.25 = 0.3536
m_gm = (0.143 × 1 × 0.143 × 1)^0.25 = (0.02045)^0.25 = 0.3790
u_gm = (0.167 × 1 × 0.167 × 1)^0.25 = (0.02789)^0.25 = 0.4082
```

**Jumlah Geometric Mean:**

| | Σ l_gm | Σ m_gm | Σ u_gm |
|-|--------|--------|--------|
| | 5.1874 | 5.6908 | 6.1718 |

---

#### Langkah 5 — Normalisasi → Bobot Fuzzy TFN

Formula normalisasi: `wᵢ.l = l_gmᵢ / Σu_gm`, `wᵢ.m = m_gmᵢ / Σm_gm`, `wᵢ.u = u_gmᵢ / Σl_gm`

| Kriteria | l_gm | wᵢ.l = l/Σu | m_gm | wᵢ.m = m/Σm | u_gm | wᵢ.u = u/Σl |
|----------|------|------------|------|------------|------|------------|
| Return | 2.2134 | **0.3586** | 2.4323 | **0.4274** | 2.6318 | **0.5073** |
| Risiko | 0.4082 | **0.0661** | 0.4472 | **0.0786** | 0.5000 | **0.0964** |
| Dividend | 2.2134 | **0.3586** | 2.4323 | **0.4274** | 2.6318 | **0.5073** |
| Stabilitas | 0.3536 | **0.0573** | 0.3790 | **0.0666** | 0.4082 | **0.0787** |

---

#### Langkah 6 — Defuzzifikasi BNP

`BNPᵢ = (wᵢ.l + wᵢ.m + wᵢ.u) / 3`

| Kriteria | l | m | u | BNP = (l+m+u)/3 |
|----------|---|---|---|----------------|
| Return | 0.3586 | 0.4274 | 0.5073 | **0.4311** |
| Risiko | 0.0661 | 0.0786 | 0.0964 | **0.0804** |
| Dividend | 0.3586 | 0.4274 | 0.5073 | **0.4311** |
| Stabilitas | 0.0573 | 0.0666 | 0.0787 | **0.0675** |
| **Jumlah** | | | | **1.0101** |

**Bobot Akhir (Ternormalisasi):** `wᵢ = BNPᵢ / Σ BNP`

| Kriteria | BNP | Bobot Akhir | Persentase |
|----------|-----|-------------|-----------|
| Return | 0.4311 | **0.4268** | 42.68% |
| Risiko | 0.0804 | **0.0796** | 7.96% |
| Dividend | 0.4311 | **0.4268** | 42.68% |
| Stabilitas | 0.0675 | **0.0668** | 6.68% |
| **Total** | | **1.0000** | **100%** |

> Return dan Dividend mendapat bobot tertinggi dan sama besar (42.68%), artinya investor dalam skenario ini memprioritaskan keuntungan finansial.

---

#### Langkah 7 — Uji Konsistensi

> **Catatan metode**: Uji konsistensi menggunakan **aproksimasi** yang lazim dalam literatur Fuzzy-AHP — yaitu nilai tengah `m` dari TFN (bukan TFN penuh) dikombinasikan dengan bobot crisp hasil BNP. Ini setara dengan menguji konsistensi preferensi inti pengambil keputusan.

**Weighted Sum Vector (WSV)** — menggunakan nilai tengah `m` matriks × bobot crisp:

```
WSV_Return = 1.0×0.4268 + 5.0×0.0796 + 1.0×0.4268 + 7.0×0.0668
           = 0.4268 + 0.3980 + 0.4268 + 0.4676 = 1.7192

WSV_Risiko = 0.2×0.4268 + 1.0×0.0796 + 0.2×0.4268 + 1.0×0.0668
           = 0.0854 + 0.0796 + 0.0854 + 0.0668 = 0.3172

WSV_Dividend = 1.0×0.4268 + 5.0×0.0796 + 1.0×0.4268 + 7.0×0.0668 = 1.7192

WSV_Stabilitas = 0.143×0.4268 + 1.0×0.0796 + 0.143×0.4268 + 1.0×0.0668
              = 0.0610 + 0.0796 + 0.0610 + 0.0668 = 0.2684
```

**λ_max:**

```
λ_max = (1/4) × [(1.7192/0.4268) + (0.3172/0.0796) + (1.7192/0.4268) + (0.2684/0.0668)]
      = (1/4) × [4.0287 + 3.9849 + 4.0287 + 4.0180]
      = (1/4) × 16.0603
      = 4.0151
```

**CI dan CR:**

```
CI = (λ_max - n) / (n - 1) = (4.0151 - 4) / (4 - 1) = 0.0151 / 3 = 0.0050

CR = CI / RI = 0.0050 / 0.90 = 0.0056
```

Karena **CR = 0.0056 < 0.10**, maka penilaian **KONSISTEN** ✅

*(Nilai eksak sistem: λ_max = 4.0143, CI = 0.0048, CR = 0.0053)*

---

#### Langkah 8 — Hitung Skor Saham

Data nilai kriteria ternormalisasi (dari data real-time / fallback):

| Saham | Return (R) | Risiko (Ri) | 1−Ri | Dividend (D) | Stabilitas (St) |
|-------|-----------|------------|------|-------------|----------------|
| HMSP | 0.7714 | 0.3755 | **0.6245** | 1.0000 | 0.9143 |
| UNVR | 0.7529 | 0.0000 | **1.0000** | 0.5094 | 1.0000 |
| MYOR | 1.0000 | 0.1419 | **0.8581** | 0.0000 | 0.9059 |
| ICBP | 0.6790 | 1.0000 | **0.0000** | 0.3019 | 0.7389 |
| KLBF | 0.0000 | 0.4640 | **0.5360** | 0.2453 | 0.0000 |

Formula skor: `S = 0.4268×R + 0.0796×(1−Ri) + 0.4268×D + 0.0668×St`

**HMSP:**
```
S = 0.4268×0.7714 + 0.0796×0.6245 + 0.4268×1.0000 + 0.0668×0.9143
  = 0.3292 + 0.0497 + 0.4268 + 0.0611
  = 0.8668
```

**UNVR:**
```
S = 0.4268×0.7529 + 0.0796×1.0000 + 0.4268×0.5094 + 0.0668×1.0000
  = 0.3213 + 0.0796 + 0.2174 + 0.0668
  = 0.6851
```

**MYOR:**
```
S = 0.4268×1.0000 + 0.0796×0.8581 + 0.4268×0.0000 + 0.0668×0.9059
  = 0.4268 + 0.0683 + 0.0000 + 0.0605
  = 0.5556
```

**ICBP:**
```
S = 0.4268×0.6790 + 0.0796×0.0000 + 0.4268×0.3019 + 0.0668×0.7389
  = 0.2898 + 0.0000 + 0.1288 + 0.0494
  = 0.4680
```

**KLBF:**
```
S = 0.4268×0.0000 + 0.0796×0.5360 + 0.4268×0.2453 + 0.0668×0.0000
  = 0.0000 + 0.0427 + 0.1047 + 0.0000
  = 0.1474
```

---

### 4.3 Hasil Ranking

Berdasarkan perhitungan di atas, ranking saham Consumer Goods adalah:

| Ranking | Kode | Skor | Status |
|---------|------|------|--------|
| 🥇 **1** | **HMSP** | **0.8668** | Sangat Direkomendasikan |
| 🥈 **2** | **UNVR** | **0.6851** | Sangat Direkomendasikan |
| 🥉 **3** | **MYOR** | **0.5556** | Stabil |
| 4 | ICBP | 0.4680 | Stabil |
| 5 | KLBF | 0.1474 | Stabil |

**Analisis:**

- **HMSP** unggul karena memiliki dividend yield tertinggi (ternormalisasi = 1.0) dan return yang baik. Dengan bobot dividend dan return masing-masing 42.68%, HMSP sangat diuntungkan oleh preferensi investor yang memprioritaskan kedua kriteria tersebut.

- **UNVR** mendapat skor tinggi terutama dari dimensi risiko (nilai terkecil = 0.0 → skor risiko = 1.0 setelah dibalik) dan stabilitas tertinggi (1.0). Cocok untuk investor konservatif.

- **KLBF** mendapat skor sangat rendah karena return dan stabilitas terendah di antara kelima saham.

### 4.4 Analisis Pengaruh Bobot

Hasil ranking sangat dipengaruhi oleh **preferensi investor** yang diinput melalui slider. Tabel berikut menunjukkan bagaimana perubahan preferensi mengubah rekomendasi:

| Skenario | Prioritas | Bobot Dominan | Saham Terbaik |
|----------|-----------|---------------|---------------|
| **A** (contoh di atas) | Return = Dividend | ~42.7% keduanya | HMSP |
| **B** | Risiko paling penting | ~50% risiko | UNVR |
| **C** | Semua kriteria sama | 25% masing-masing | HMSP |
| **D** | Return dominan | ~52% return | MYOR |

Hal ini menunjukkan sistem bersifat **adaptif**: rekomendasi berubah sesuai profil risiko dan tujuan investasi pengguna.

---

## BAB V KESIMPULAN DAN SARAN

### 5.1 Kesimpulan

1. Sistem InvestRank berhasil diimplementasikan sebagai aplikasi web berbasis Python/Flask yang mampu meranking 5 saham Consumer Goods menggunakan metode Fuzzy-AHP.

2. Penerapan **TFN** dalam matriks perbandingan berpasangan berhasil merepresentasikan ketidakpastian penilaian manusia, yang menjadi kelemahan utama AHP konvensional. Dengan TFN, setiap penilaian dinyatakan sebagai rentang `(l, m, u)` bukan angka tunggal.

3. Metode **geometric mean Buckley** terbukti efektif menghitung bobot fuzzy dari matriks TFN, dan defuzzifikasi **BNP** menghasilkan bobot crisp yang dapat langsung digunakan dalam kalkulasi skor.

4. Uji konsistensi menggunakan **CR** memastikan kualitas input pengguna. Dari beberapa sesi pengujian, diperoleh nilai CR antara 0.000 hingga 0.243, di mana penilaian yang konsisten (CR < 0.10) menghasilkan rekomendasi yang lebih dapat dipercaya.

5. Integrasi **data real-time Yahoo Finance** memastikan nilai kriteria selalu mencerminkan kondisi pasar terkini, meskipun fallback statis tersedia saat koneksi tidak tersedia.

6. Hasil sistem menunjukkan bahwa rekomendasi saham **sangat dipengaruhi oleh preferensi pengguna**. Preferensi yang berfokus pada dividend dan return cenderung merekomendasikan HMSP, sementara preferensi risiko rendah merekomendasikan UNVR.

### 5.2 Saran

1. **Penambahan Saham**: Sistem dapat diperluas dengan lebih banyak emiten dari sektor Consumer Goods atau sektor lain untuk memberikan pilihan yang lebih beragam.

2. **Penambahan Kriteria**: Kriteria tambahan seperti *Price-to-Earnings Ratio (PER)*, *Price-to-Book Value (PBV)*, atau *Market Capitalization* dapat dipertimbangkan untuk analisis yang lebih komprehensif.

3. **Metode AHP Alternatif**: Dapat dicoba metode lain seperti *Chang's Extent Analysis* atau *FAHP with trapezoidal fuzzy number* untuk dibandingkan hasilnya.

4. **Penyimpanan Database**: Saat ini riwayat disimpan dalam file JSON lokal. Pengembangan lebih lanjut dapat menggunakan database relasional (SQLite/PostgreSQL) untuk skalabilitas.

5. **Deployment**: Sistem dapat di-deploy ke platform cloud (Heroku, Railway, atau VPS) agar dapat diakses publik.

6. **Validasi dengan Pakar**: Rekomendasi sistem sebaiknya divalidasi dengan pendapat analis saham atau pakar keuangan untuk mengukur tingkat akurasi praktisnya.

---

## DAFTAR PUSTAKA

1. Saaty, T. L. (1980). *The Analytic Hierarchy Process: Planning, Priority Setting, Resource Allocation*. McGraw-Hill.

2. Buckley, J. J. (1985). Fuzzy Hierarchical Analysis. *Fuzzy Sets and Systems*, 17(3), 233–247.

3. Chang, D. Y. (1996). Applications of the Extent Analysis Method on Fuzzy AHP. *European Journal of Operational Research*, 95(3), 649–655.

4. Zadeh, L. A. (1965). Fuzzy Sets. *Information and Control*, 8(3), 338–353.

5. Kusumadewi, S., & Purnomo, H. (2010). *Aplikasi Logika Fuzzy untuk Pendukung Keputusan* (Edisi 2). Graha Ilmu, Yogyakarta.

6. Turban, E., Aronson, J. E., & Liang, T.-P. (2005). *Decision Support Systems and Intelligent Systems* (7th ed.). Pearson Prentice Hall.

7. Bursa Efek Indonesia. (2026). Data Emiten Sektor Consumer Non-Cyclicals. Diakses dari https://www.idx.co.id

8. Yahoo Finance. (2026). Historical Data & Financial Information. Diakses melalui library `yfinance` (Python).

9. Gkamas, V. (2023). *yfinance: Yahoo! Finance market data downloader* (v0.2.x). Python Package Index (PyPI).

10. Pallets Projects. (2024). *Flask: A lightweight WSGI web application framework* (v3.x). Python Package Index (PyPI).

11. Kahraman, C., Cebeci, U., & Ulukan, Z. (2003). Multi-criteria supplier selection using fuzzy AHP. *Logistics Information Management*, 16(6), 382–394. *(Referensi untuk pendekatan defuzzified consistency check dalam Fuzzy-AHP.)*

---

*Laporan ini dibuat sebagai dokumentasi Proyek Akhir Mata Kuliah Logika Fuzzy (SCR), Program Studi Teknik Informatika, Universitas Teknologi Yogyakarta — 2026.*
