# =========================
# FILE : fuzzy_ahp.py
# Logika Fuzzy AHP
# Metode: Triangular Fuzzy Number (TFN) + BNP Defuzzifikasi
# =========================

import math

# ──────────────────────────────────────────────
# Tabel konversi skala Saaty → TFN (l, m, u)
# Reciprocal dihitung otomatis saat build matriks
# ──────────────────────────────────────────────
FUZZY_SCALE = {
    1: (1.0, 1.0, 1.0),
    2: (1.0, 2.0, 3.0),
    3: (2.0, 3.0, 4.0),
    4: (3.0, 4.0, 5.0),
    5: (4.0, 5.0, 6.0),
    6: (5.0, 6.0, 7.0),
    7: (6.0, 7.0, 8.0),
    8: (7.0, 8.0, 9.0),
    9: (8.0, 9.0, 9.0),
}


def crisp_to_tfn(value: int) -> tuple:
    """
    Konversi nilai crisp integer 1-9 ke Triangular Fuzzy Number.
    Return: (l, m, u)
    """
    v = max(1, min(9, int(value)))
    return FUZZY_SCALE[v]


def tfn_reciprocal(tfn: tuple) -> tuple:
    """
    Hitung reciprocal TFN: (l,m,u)^-1 = (1/u, 1/m, 1/l)
    """
    l, m, u = tfn
    return (1.0 / u, 1.0 / m, 1.0 / l)


def tfn_multiply(a: tuple, b: tuple) -> tuple:
    """Perkalian dua TFN: (a1*b1, a2*b2, a3*b3)"""
    return (a[0] * b[0], a[1] * b[1], a[2] * b[2])


def tfn_power(tfn: tuple, exp: float) -> tuple:
    """Pangkat TFN: (l^exp, m^exp, u^exp)"""
    return (tfn[0] ** exp, tfn[1] ** exp, tfn[2] ** exp)


def build_fuzzy_matrix(values: list, n: int = 4) -> list:
    """
    Bangun matriks perbandingan fuzzy n×n dari list values (6 pasangan).

    Urutan pasangan (n=4 kriteria):
      [0] Return vs Risiko
      [1] Return vs Dividend
      [2] Return vs Stabilitas
      [3] Risiko vs Dividend
      [4] Risiko vs Stabilitas
      [5] Dividend vs Stabilitas

    Nilai slider UI: 1–9, tengah (5) = sama penting.
    Konversi ke skala Saaty:
      slider=5      → Saaty 1  (sama penting)
      jarak 1 step  → Saaty 3  (sedikit lebih penting)
      jarak 2 step  → Saaty 5  (cukup penting)
      jarak 3 step  → Saaty 7  (sangat penting)
      jarak 4 step  → Saaty 9  (mutlak penting)
      Formula: saaty = 1 + 2 * |slider - 5|

    Return: matriks n×n berisi TFN (l, m, u)
    """
    matrix = [[(1.0, 1.0, 1.0)] * n for _ in range(n)]

    pairs = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3),
        (2, 3),
    ]

    for idx, (i, j) in enumerate(pairs):
        v = int(values[idx])
        if v == 5:
            # sama penting → diagonal TFN
            matrix[i][j] = (1.0, 1.0, 1.0)
            matrix[j][i] = (1.0, 1.0, 1.0)
        elif v > 5:
            # kriteria i (sisi kanan slider) lebih penting
            saaty = 1 + 2 * (v - 5)
            tfn = crisp_to_tfn(saaty)
            matrix[i][j] = tfn
            matrix[j][i] = tfn_reciprocal(tfn)
        else:
            # kriteria j (sisi kiri slider) lebih penting
            saaty = 1 + 2 * (5 - v)
            tfn = crisp_to_tfn(saaty)
            matrix[j][i] = tfn
            matrix[i][j] = tfn_reciprocal(tfn)

    return matrix


def geometric_mean_row(row: list) -> tuple:
    """
    Hitung geometric mean setiap komponen TFN pada satu baris.
    Return: TFN (l_gm, m_gm, u_gm)
    """
    n = len(row)
    l_gm = math.prod(cell[0] for cell in row) ** (1.0 / n)
    m_gm = math.prod(cell[1] for cell in row) ** (1.0 / n)
    u_gm = math.prod(cell[2] for cell in row) ** (1.0 / n)
    return (l_gm, m_gm, u_gm)


def fuzzy_weights_from_matrix(matrix: list) -> list:
    """
    Hitung bobot fuzzy dari matriks TFN menggunakan geometric mean method.
    Return: list TFN bobot per kriteria [(l,m,u), ...]
    """
    n = len(matrix)
    gm_rows = [geometric_mean_row(matrix[i]) for i in range(n)]

    # Jumlah semua geometric mean per komponen
    sum_l = sum(r[0] for r in gm_rows)
    sum_m = sum(r[1] for r in gm_rows)
    sum_u = sum(r[2] for r in gm_rows)

    # Normalisasi: bagi dengan (sum_u, sum_m, sum_l) — perhatikan urutan terbalik
    weights_tfn = []
    for (l, m, u) in gm_rows:
        wl = l / sum_u
        wm = m / sum_m
        wu = u / sum_l
        weights_tfn.append((wl, wm, wu))

    return weights_tfn


def defuzzify_bnp(weights_tfn: list) -> list:
    """
    Defuzzifikasi TFN ke nilai crisp menggunakan metode BNP (Best Non-fuzzy Performance).
    Formula: BNP = (u - l + m - l) / 3 + l = (l + m + u) / 3
    Return: list bobot crisp yang sudah dinormalisasi
    """
    crisp = [(l + m + u) / 3.0 for (l, m, u) in weights_tfn]
    total = sum(crisp)
    return [w / total for w in crisp]


def calculate_fuzzy_ahp(values: list) -> dict:
    """
    Fungsi utama: hitung seluruh proses Fuzzy AHP dari input values.

    Args:
        values: list 6 integer (1-9) dari wizard perbandingan

    Return:
        dict dengan kunci:
          - bobot      : dict {return, risiko, dividend, stabilitas} bobot crisp
          - bobot_tfn  : dict {return, risiko, dividend, stabilitas} bobot TFN
          - tfn_matrix : matriks TFN 4×4 (untuk ditampilkan)
          - ci         : Consistency Index (approximate dari defuzzified)
          - cr         : Consistency Ratio
          - consistent : bool
          - method     : 'fuzzy-ahp'
    """
    KRITERIA = ['return', 'risiko', 'dividend', 'stabilitas']
    RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32}
    n = 4

    # 1. Bangun matriks fuzzy
    matrix = build_fuzzy_matrix(values, n)

    # 2. Hitung bobot TFN
    weights_tfn = fuzzy_weights_from_matrix(matrix)

    # 3. Defuzzifikasi → bobot crisp
    weights_crisp = defuzzify_bnp(weights_tfn)

    # 4. Hitung CI/CR dari bobot crisp (approx konsistensi)
    # Weighted sum vector
    ws = [0.0] * n
    for i in range(n):
        for j in range(n):
            # Gunakan nilai m (middle) matriks untuk approx
            ws[i] += matrix[i][j][1] * weights_crisp[j]

    lambda_max = sum(
        ws[i] / weights_crisp[i] if weights_crisp[i] != 0 else 0.0
        for i in range(n)
    ) / n
    ci = (lambda_max - n) / (n - 1)
    cr = ci / RI[n]

    # 5. Susun output
    bobot = {KRITERIA[i]: round(weights_crisp[i], 6) for i in range(n)}
    bobot_tfn = {
        KRITERIA[i]: {
            'l': round(weights_tfn[i][0], 6),
            'm': round(weights_tfn[i][1], 6),
            'u': round(weights_tfn[i][2], 6),
        }
        for i in range(n)
    }

    # Konversi matrix ke format JSON-able
    matrix_out = []
    for row in matrix:
        matrix_out.append([
            {'l': round(c[0], 4), 'm': round(c[1], 4), 'u': round(c[2], 4)}
            for c in row
        ])

    return {
        'bobot':     bobot,
        'bobot_tfn': bobot_tfn,
        'matrix':    matrix_out,
        'lambda_max': round(lambda_max, 6),
        'ci':        round(ci, 6),
        'cr':        round(cr, 6),
        'consistent': cr <= 0.10,
        'method':    'fuzzy-ahp',
    }
