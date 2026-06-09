# =========================
# FILE : app.py
# Single-page — semua section di dashboard.html
# =========================

import os
from datetime import datetime

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, jsonify
)

from fuzzy_ahp   import calculate_fuzzy_ahp
from models  import get_all_saham, ranking_saham, get_cache_info, _realtime_cache
from history import (
    load_history, save_history_entry,
    get_history_entry, delete_history_entry, clear_history,
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'investrank-secret-2025')


# ─────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────

def get_comparison_data():
    return session.get('comparison', None)


def _redirect_to(section: str):
    """Simpan target scroll ke session lalu redirect ke dashboard."""
    session['_scroll_to'] = section
    return redirect(url_for('dashboard'))


# ─────────────────────────────────────────
# SATU-SATUNYA HALAMAN
# ─────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    stocks     = get_all_saham(realtime=True, include_internal=True)
    for s in stocks:
        s['risiko_val']     = round(s.get('_risiko', 0) * 100, 1)
        s['stabilitas_val'] = round(s.get('_stabilitas', 0) * 100, 1)
    comparison = get_comparison_data()
    ahp        = comparison.get('fuzzy') if comparison else None
    ranking    = comparison.get('ranking_fuzzy') if comparison else None
    cache_info = get_cache_info()
    history    = load_history()
    scroll_to  = session.pop('_scroll_to', None)
    return render_template(
        'dashboard.html',
        stocks=stocks,
        comparison=comparison,
        ahp=ahp,
        ranking=ranking,
        total_record=len(stocks),
        cache_info=cache_info,
        history=history,
        scroll_to=scroll_to,
        active_page='dashboard',
    )


# ─────────────────────────────────────────
# REDIRECT SEMUA ROUTE LAMA KE SECTION
# ─────────────────────────────────────────

@app.route('/saham')
def saham():
    return _redirect_to('sec-saham')


@app.route('/kriteria')
def kriteria():
    return _redirect_to('sec-kriteria')


@app.route('/ahp')
def ahp():
    return _redirect_to('sec-ahp')


@app.route('/hasil')
def hasil():
    comparison = get_comparison_data()
    if not comparison:
        return _redirect_to('sec-ahp')
    return _redirect_to('sec-hasil')


# ─────────────────────────────────────────
# API : SUBMIT AHP
# ─────────────────────────────────────────

@app.route('/ahp/submit', methods=['POST'])
def submit_ahp():
    data   = request.get_json(silent=True) or {}
    values = data.get('values', [5, 5, 5, 5, 5, 5])

    if len(values) != 6:
        return jsonify({'error': 'Butuh tepat 6 nilai perbandingan'}), 400

    try:
        values = [max(1, min(9, int(v))) for v in values]
    except (ValueError, TypeError):
        return jsonify({'error': 'Nilai harus integer 1–9'}), 400

    fuzzy_result  = calculate_fuzzy_ahp(values)
    saham_list    = get_all_saham(realtime=True, include_internal=True)
    ranking_fuzzy = ranking_saham(fuzzy_result['bobot'], saham_data=saham_list)

    comparison_data = {
        'fuzzy':         fuzzy_result,
        'ranking_fuzzy': ranking_fuzzy,
        'input_values':  values,
        'timestamp':     datetime.now().strftime('%d %b %Y, %H:%M:%S'),
    }
    session['comparison']  = comparison_data
    session['_scroll_to']  = 'sec-hasil'
    save_history_entry(comparison_data)

    return jsonify({
        'status':           'ok',
        'cr_fuzzy':         fuzzy_result['cr'],
        'consistent_fuzzy': fuzzy_result['consistent'],
        'top_fuzzy':        ranking_fuzzy[0]['kode'] if ranking_fuzzy else '-',
        'redirect':         url_for('dashboard'),
    })


@app.route('/ahp/reset')
def reset_ahp():
    session.pop('comparison', None)
    return _redirect_to('sec-ahp')


# ─────────────────────────────────────────
# RIWAYAT
# ─────────────────────────────────────────

@app.route('/riwayat/hapus-semua')
def hapus_semua_riwayat():
    clear_history()
    return _redirect_to('sec-ahp')


@app.route('/riwayat/<entry_id>')
def lihat_riwayat(entry_id):
    entry = get_history_entry(entry_id)
    if not entry:
        return _redirect_to('sec-ahp')
    session['comparison'] = entry['comparison']
    return _redirect_to('sec-hasil')


@app.route('/riwayat/<entry_id>/hapus')
def hapus_riwayat(entry_id):
    delete_history_entry(entry_id)
    return _redirect_to('sec-ahp')


# ─────────────────────────────────────────
# API
# ─────────────────────────────────────────

@app.route('/api/refresh-cache')
def refresh_cache():
    _realtime_cache['data'] = None
    _realtime_cache['ts']   = 0.0
    return jsonify({'status': 'ok', 'message': 'Cache dikosongkan.'})


# ─────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5001)
