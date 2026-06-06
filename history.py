# =========================
# FILE : history.py
# Simpan & muat riwayat analisis Fuzzy-AHP ke file JSON
# =========================

import json
import os
import uuid
from datetime import datetime

_HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'riwayat.json')
_MAX_ENTRIES  = 30


def load_history() -> list:
    if not os.path.exists(_HISTORY_FILE):
        return []
    try:
        with open(_HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _write_history(history: list) -> None:
    with open(_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def save_history_entry(comparison: dict) -> str:
    """Simpan satu entry analisis ke riwayat; kembalikan id entry."""
    history  = load_history()
    entry_id = uuid.uuid4().hex[:8]
    fuzzy    = comparison.get('fuzzy', {})
    ranking  = comparison.get('ranking_fuzzy', [])

    entry = {
        'id':        entry_id,
        'timestamp': comparison.get('timestamp', datetime.now().strftime('%d %b %Y, %H:%M:%S')),
        'comparison': comparison,
        'summary': {
            'cr':           fuzzy.get('cr', 0),
            'consistent':   fuzzy.get('consistent', False),
            'top_saham':    ranking[0]['kode'] if ranking else '-',
            'top_skor':     ranking[0]['skor'] if ranking else 0,
            'input_values': comparison.get('input_values', []),
            'bobot':        fuzzy.get('bobot', {}),
        },
    }

    history.insert(0, entry)
    if len(history) > _MAX_ENTRIES:
        history = history[:_MAX_ENTRIES]

    try:
        _write_history(history)
    except Exception:
        pass

    return entry_id


def get_history_entry(entry_id: str):
    for entry in load_history():
        if entry.get('id') == entry_id:
            return entry
    return None


def delete_history_entry(entry_id: str) -> bool:
    history     = load_history()
    new_history = [h for h in history if h.get('id') != entry_id]
    if len(new_history) == len(history):
        return False
    try:
        _write_history(new_history)
        return True
    except Exception:
        return False


def clear_history() -> None:
    try:
        _write_history([])
    except Exception:
        pass
