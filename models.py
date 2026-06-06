# =========================
# FILE : models.py
# Data saham & fungsi ranking
# =========================

import math
import time
from datetime import datetime
import yfinance as yf

# Cache real-time data selama 5 menit agar tidak fetch ulang tiap request
_CACHE_TTL = 300  # detik
_realtime_cache: dict = {'data': None, 'ts': 0.0}


# ──────────────────────────────────────────────
# Data saham Consumer Goods (simulasi)
# Ganti dengan query DB sesuai setup Anda
# ──────────────────────────────────────────────
SAHAM_DATA = [
    {
        'kode':       'UNVR',
        'keterangan': 'Unilever Indonesia',
        'harga':      1570,
        'return_pct': -4.27,
        'dividend':   '4.20%',
        # Nilai kriteria dinormalisasi 0-1 (fallback jika Yahoo Finance tidak tersedia)
        '_return':     0.98,
        '_risiko':     0.00,
        '_dividend':   0.51,
        '_stabilitas': 0.65,
    },
    {
        'kode':       'ICBP',
        'keterangan': 'Indofood CBP Sukses Makmur',
        'harga':      6450,
        'return_pct': -4.09,
        'dividend':   '3.10%',
        '_return':     1.00,
        '_risiko':     0.26,
        '_dividend':   0.30,
        '_stabilitas': 1.00,
    },
    {
        'kode':       'KLBF',
        'keterangan': 'Kalbe Farma',
        'harga':      695,
        'return_pct': -15.93,
        'dividend':   '2.80%',
        '_return':     0.00,
        '_risiko':     0.70,
        '_dividend':   0.25,
        '_stabilitas': 0.00,
    },
    {
        'kode':       'MYOR',
        'keterangan': 'Mayora Indah',
        'harga':      1690,
        'return_pct': -5.32,
        'dividend':   '1.50%',
        '_return':     0.90,
        '_risiko':     0.86,
        '_dividend':   0.00,
        '_stabilitas': 0.96,
    },
    {
        'kode':       'HMSP',
        'keterangan': 'HM Sampoerna',
        'harga':      630,
        'return_pct': -11.39,
        'dividend':   '6.80%',
        '_return':     0.38,
        '_risiko':     1.00,
        '_dividend':   1.00,
        '_stabilitas': 0.89,
    },
]

YAHOO_TICKERS = {
    'UNVR': 'UNVR.JK',
    'ICBP': 'ICBP.JK',
    'KLBF': 'KLBF.JK',
    'MYOR': 'MYOR.JK',
    'HMSP': 'HMSP.JK',
}


def _normalize(values: list, invert: bool = False) -> list:
    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [0.5 for _ in values]
    normalized = [(v - minimum) / (maximum - minimum) for v in values]
    return [1.0 - x if invert else x for x in normalized]


def _format_dividend(value: float) -> str:
    if value is None:
        return '0.00%'
    return f"{value * 100:.2f}%"


def _fetch_realtime_saham_data() -> list:
    now = time.time()
    if _realtime_cache['data'] is not None and (now - _realtime_cache['ts']) < _CACHE_TTL:
        return _realtime_cache['data']

    symbols = list(YAHOO_TICKERS.values())
    try:
        history = yf.download(
            tickers=symbols,
            period='1mo',
            interval='1d',
            group_by='ticker',
            threads=False,
            progress=False,
        )
        tickers = yf.Tickers(' '.join(symbols))
    except Exception:
        return []

    realtime = []
    returns = []
    volatilities = []
    dividends = []
    stabilities = []

    for code, symbol in YAHOO_TICKERS.items():
        info = {}
        price = None
        prev_close = None
        ticker = tickers.tickers.get(symbol)
        if ticker is not None:
            try:
                info = ticker.info or {}
            except Exception:
                info = {}

        price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('previousClose') or 0.0
        prev_close = info.get('regularMarketPreviousClose') or info.get('previousClose') or price

        close_series = None
        if isinstance(history, dict) and symbol in history:
            close_series = history[symbol].get('Close')
        elif hasattr(history, 'columns') and symbol in history.columns.get_level_values(0):
            close_series = history[symbol]['Close']

        monthly_return = 0.0
        volatility = 0.0
        stability = 0.0

        history_dates = []
        history_values = []
        if close_series is not None:
            close_series = close_series.dropna()
            if len(close_series) >= 2:
                monthly_return = (close_series.iloc[-1] / close_series.iloc[0] - 1.0) * 100.0
                daily_returns = close_series.pct_change().dropna()
                volatility = float(daily_returns.std() or 0.0)
                _max_price = float(close_series.max())
                stability = 1.0 - ((float(close_series.max()) - float(close_series.min())) / _max_price) if _max_price > 0 else 0.0
                history_dates = [d.strftime('%d %b') for d in close_series.index[-30:]]
                history_values = [float(v) for v in close_series.iloc[-30:]]

        dividend_yield = info.get('trailingAnnualDividendYield')
        if dividend_yield is None or dividend_yield == 0.0:
            # Fallback ke SAHAM_DATA jika Yahoo Finance tidak memiliki data
            default_stock = next((s for s in SAHAM_DATA if s['kode'] == code), None)
            if default_stock:
                dividend_str = default_stock.get('dividend', '0.00%')
                dividend_yield = float(dividend_str.rstrip('%')) / 100.0
            else:
                dividend_yield = 0.0

        realtime.append({
            'kode': code,
            'harga': float(price),
            'return_pct': round(monthly_return, 2),
            'dividend': _format_dividend(dividend_yield),
            '_raw_return': monthly_return,
            '_raw_risiko': volatility,
            '_raw_dividend': dividend_yield * 100.0,
            '_raw_stabilitas': stability,
            'history_dates': history_dates,
            'history_values': history_values,
        })
        returns.append(monthly_return)
        volatilities.append(volatility)
        dividends.append(dividend_yield * 100.0)
        stabilities.append(stability)

    norm_returns = _normalize(returns)
    # Simpan risiko sebagai cost criterion: 0 = risiko rendah, 1 = risiko tinggi.
    # Pembalikan menjadi skor benefit dilakukan sekali saja di ranking_saham().
    norm_risks = _normalize(volatilities)
    norm_dividends = _normalize(dividends)
    norm_stabilities = _normalize(stabilities)

    for idx, item in enumerate(realtime):
        item['_return'] = round(norm_returns[idx], 6)
        item['_risiko'] = round(norm_risks[idx], 6)
        item['_dividend'] = round(norm_dividends[idx], 6)
        item['_stabilitas'] = round(norm_stabilities[idx], 6)

    if realtime and any(s['harga'] > 0 for s in realtime):
        _realtime_cache['data'] = realtime
        _realtime_cache['ts'] = time.time()
    return realtime


def get_cache_info() -> dict:
    """Return info tentang cache data real-time."""
    ts = _realtime_cache['ts']
    has_data = _realtime_cache['data'] is not None
    age = int(time.time() - ts) if ts > 0 else None
    return {
        'has_data': has_data,
        'is_realtime': has_data and ts > 0,
        'age_seconds': age,
        'last_updated': datetime.fromtimestamp(ts).strftime('%d %b %Y, %H:%M:%S') if ts > 0 else None,
        'next_refresh_seconds': max(0, _CACHE_TTL - age) if age is not None else 0,
    }


def ranking_saham(bobot: dict, saham_data: list = None) -> list:
    """
    Hitung skor akhir tiap saham berdasarkan bobot AHP/Fuzzy-AHP.

    Formula skor:
      skor = w_return   * _return
           + w_risiko   * (1 - _risiko)   ← cost criterion, dibalik
           + w_dividend * _dividend
           + w_stabilitas * _stabilitas

    Return: list saham diurutkan dari skor tertinggi
    """
    if saham_data is None:
        saham_data = SAHAM_DATA

    hasil = []
    for s in saham_data:
        skor = (
            bobot.get('return',     0) * s.get('_return', 0)
            + bobot.get('risiko',   0) * (1.0 - s.get('_risiko', 0))
            + bobot.get('dividend', 0) * s.get('_dividend', 0)
            + bobot.get('stabilitas', 0) * s.get('_stabilitas', 0)
        )
        hasil.append({
            'kode':   s['kode'],
            'skor':   round(skor, 6),
            'detail': {
                'return':     s.get('_return', 0),
                'risiko':     s.get('_risiko', 0),
                'dividend':   s.get('_dividend', 0),
                'stabilitas': s.get('_stabilitas', 0),
            },
        })

    hasil.sort(key=lambda x: x['skor'], reverse=True)
    return hasil


def get_all_saham(realtime: bool = False, include_internal: bool = False) -> list:
    """Return semua data saham, optionally dengan realtime values and internal scoring values."""
    keys_public = ['kode', 'keterangan', 'harga', 'return_pct', 'dividend']
    saham = [dict(s) for s in SAHAM_DATA]

    if realtime:
        realtime_data = _fetch_realtime_saham_data()
        if realtime_data:
            for s in saham:
                match = next((item for item in realtime_data if item['kode'] == s['kode']), None)
                if match:
                    s.update(match)

    if include_internal:
        return saham
    return [{k: s[k] for k in keys_public} for s in saham]
