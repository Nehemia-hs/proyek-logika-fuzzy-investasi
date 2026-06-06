/* =========================
   FILE : fuzzy_ahp.js
   Wizard Fuzzy-AHP — satu input, satu output
   Urutan: 3 perbandingan langsung → 3 turunan (transitif)
========================= */

document.addEventListener('DOMContentLoaded', function () {

    /* ── PASANGAN KRITERIA
       3 langkah pertama = rantai langsung (transitif)
       3 langkah terakhir = turunan yang dihitung otomatis ── */
    var pairs = [
        ['Return',   'Risiko'],      // step 0  langsung
        ['Risiko',   'Dividend'],    // step 1  langsung
        ['Dividend', 'Stabilitas'],  // step 2  langsung
        ['Return',   'Dividend'],    // step 3  turunan = step0 × step1
        ['Return',   'Stabilitas'],  // step 4  turunan = step0 × step1 × step2
        ['Risiko',   'Stabilitas'],  // step 5  turunan = step1 × step2
    ];

    /* Backend mengharapkan urutan (0,1)(0,2)(0,3)(1,2)(1,3)(2,3)
       Map: wizard index → backend index */
    var wizardToBackend = [0, 3, 5, 1, 2, 4];

    /* Tabel TFN per skala Saaty 1–9 */
    var SAATY_TFN = {
        1:[1,1,1], 2:[1,2,3], 3:[2,3,4], 4:[3,4,5],
        5:[4,5,6], 6:[5,6,7], 7:[6,7,8], 8:[7,8,9], 9:[8,9,9],
    };

    /* Konversi slider 1-9 (tengah=5 sama penting) → Saaty
       jarak 1 step = Saaty 3, 2 = 5, 3 = 7, 4 = 9 */
    function sliderToSaaty(v) {
        if (v === 5) return 1;
        return 1 + 2 * Math.abs(v - 5);
    }

    /* Rasio numerik dari slider: >1 jika pairs[step][0] lebih penting */
    function sliderToRatio(v) {
        if (v === 5) return 1.0;
        var s = sliderToSaaty(v);
        return v > 5 ? s : 1.0 / s;
    }

    /* Rasio → slider integer paling dekat (1-9) */
    function ratioToSlider(ratio) {
        if (ratio > 0.85 && ratio < 1.18) return 5;
        if (ratio > 1) {
            var s = Math.min(9, Math.max(1, Math.round(ratio)));
            return Math.min(9, Math.round(5 + (s - 1) / 2));
        } else {
            var s2 = Math.min(9, Math.max(1, Math.round(1 / ratio)));
            return Math.max(1, Math.round(5 - (s2 - 1) / 2));
        }
    }

    /* Hitung saran nilai konsisten untuk steps 3-5 dari tiga langkah langsung */
    function computeSuggestions() {
        var r01 = sliderToRatio(vals[0]); // Return / Risiko
        var r12 = sliderToRatio(vals[1]); // Risiko / Dividend
        var r23 = sliderToRatio(vals[2]); // Dividend / Stabilitas
        suggestions[3] = ratioToSlider(r01 * r12);
        suggestions[4] = ratioToSlider(r01 * r12 * r23);
        suggestions[5] = ratioToSlider(r12 * r23);
    }

    var vals        = [5, 5, 5, 5, 5, 5];
    var suggestions = [5, 5, 5, 5, 5, 5];
    /* Catat apakah user sudah override nilai turunan */
    var userOverride = [false, false, false, false, false, false];
    var step = 0;

    /* ── DOM ── */
    var elStep     = document.getElementById('stepNow');
    var elTitle    = document.getElementById('questionTitle');
    var elLeft     = document.getElementById('leftLabel');
    var elRight    = document.getElementById('rightLabel');
    var elSlider   = document.getElementById('ahpSlider');
    var elProgress = document.getElementById('progressFill');
    var elPreviewV = document.getElementById('previewVal');
    var elDots     = document.getElementById('ahpStepDots');
    var elTFNL     = document.getElementById('tfnL');
    var elTFNM     = document.getElementById('tfnM');
    var elTFNU     = document.getElementById('tfnU');
    var elCrispVal = document.getElementById('crispVal');
    var elStrength = document.getElementById('decisionStrength');
    var elHint     = document.getElementById('consistencyHint');
    var btnNext    = document.getElementById('nextBtn');
    var btnPrev    = document.getElementById('prevBtn');

    if (!elSlider) return;

    /* ── DOTS ── */
    function buildDots() {
        if (!elDots) return;
        elDots.innerHTML = '';
        pairs.forEach(function (_, i) {
            var d = document.createElement('div');
            d.className = 'ahp-dot'
                + (i < step  ? ' done'
                : i === step ? ' active' : '');
            elDots.appendChild(d);
        });
    }

    /* ── PREVIEW ── */
    function updatePreview() {
        var v     = parseInt(elSlider.value);
        var saaty = sliderToSaaty(v);
        var tfn   = SAATY_TFN[saaty] || [1, 1, 1];
        var strength;

        if (saaty === 1) {
            strength = 'Netral';
        } else if (saaty === 3) {
            strength = 'Sedikit lebih penting';
        } else if (saaty === 5) {
            strength = 'Lebih penting';
        } else if (saaty === 7) {
            strength = 'Sangat lebih penting';
        } else {
            strength = 'Mutlak lebih penting';
        }

        var txt;
        if (v === 5) {
            txt = 'Kedua kriteria <strong>sama penting</strong>';
        } else if (v > 5) {
            txt = '<strong>' + pairs[step][0] + '</strong> lebih penting ('
                + saaty + '&times;) dari ' + pairs[step][1];
        } else {
            txt = '<strong>' + pairs[step][1] + '</strong> lebih penting ('
                + saaty + '&times;) dari ' + pairs[step][0];
        }
        if (elPreviewV) elPreviewV.innerHTML = txt;
        if (elStrength) elStrength.textContent = strength;

        if (elTFNL) elTFNL.textContent = tfn[0].toFixed(1);
        if (elTFNM) elTFNM.textContent = tfn[1].toFixed(1);
        if (elTFNU) elTFNU.textContent = tfn[2].toFixed(1);
        if (elCrispVal) elCrispVal.textContent = saaty;
    }

    /* ── HINT KONSISTENSI (muncul di step 3-5) ── */
    function updateHint() {
        if (!elHint) return;
        if (step < 3) { elHint.style.display = 'none'; return; }

        var s     = suggestions[step];
        var saaty = sliderToSaaty(s);
        var lbl;
        if (s === 5) {
            lbl = 'sama penting';
        } else if (s > 5) {
            lbl = pairs[step][0] + ' ' + saaty + '× lebih penting';
        } else {
            lbl = pairs[step][1] + ' ' + saaty + '× lebih penting';
        }
        elHint.style.display = '';
        elHint.innerHTML =
            '<i class="fa-solid fa-wand-magic-sparkles" style="margin-right:6px"></i>'
            + 'Nilai konsisten yang disarankan: <strong>' + lbl + '</strong>'
            + ' &nbsp;<span style="opacity:.6;font-size:12px">(sudah diisi otomatis)</span>';
    }

    /* ── RENDER STEP ── */
    function renderStep(isForward) {
        if (elStep)   elStep.textContent  = step + 1;
        if (elTitle)  elTitle.textContent = pairs[step][0] + ' vs ' + pairs[step][1];
        if (elLeft)   elLeft.textContent  = pairs[step][1];
        if (elRight)  elRight.textContent = pairs[step][0];

        /* Auto-fill nilai konsisten untuk step turunan jika user belum override */
        if (step >= 3 && isForward !== false && !userOverride[step]) {
            vals[step] = suggestions[step];
        }

        elSlider.value = vals[step];

        if (elProgress)
            elProgress.style.width = ((step + 1) / pairs.length * 100) + '%';

        buildDots();
        updatePreview();
        updateHint();

        if (btnNext) {
            if (step === pairs.length - 1) {
                btnNext.innerHTML =
                    '<i class="fa-solid fa-calculator"></i> Hitung Fuzzy-AHP';
                if (typeof window._updateSummary === 'function') window._updateSummary(vals);
            } else {
                btnNext.innerHTML =
                    'Selanjutnya <i class="fa-solid fa-arrow-right"></i>';
            }
        }
    }

    /* ── EVENTS ── */
    elSlider.addEventListener('input', function () {
        vals[step] = parseInt(this.value);
        if (step >= 3) userOverride[step] = true;
        updatePreview();
        if (step === pairs.length - 1 && typeof window._updateSummary === 'function') {
            window._updateSummary(vals);
        }
    });

    if (btnNext) {
        btnNext.addEventListener('click', function () {
            if (step < pairs.length - 1) {
                /* Saat meninggalkan step 2 → hitung saran untuk step 3-5 */
                if (step === 2) computeSuggestions();
                step++;
                renderStep(true);
            } else {
                submitAHP();
            }
        });
    }

    if (btnPrev) {
        btnPrev.addEventListener('click', function () {
            if (step > 0) { step--; renderStep(false); }
        });
    }

    /* ── SUBMIT — remap urutan wizard → urutan backend lalu POST ── */
    function submitAHP() {
        if (btnNext) {
            btnNext.disabled = true;
            btnNext.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i>'
                + ' Menghitung Fuzzy-AHP...';
        }

        /* Remap: wizard[i] → backend[wizardToBackend[i]] */
        var backendVals = [0, 0, 0, 0, 0, 0];
        for (var wi = 0; wi < 6; wi++) {
            backendVals[wizardToBackend[wi]] = vals[wi];
        }

        fetch('/ahp/submit', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ values: backendVals }),
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            if (data.status === 'ok') {
                window.location.href = data.redirect || '/dashboard';
            } else {
                alert('Error: ' + (data.error || 'Terjadi kesalahan.'));
                resetBtn();
            }
        })
        .catch(function (err) {
            resetBtn();
            showErrorToast('Koneksi gagal. Periksa jaringan Anda dan coba lagi.');
            console.error('submitAHP fetch error:', err);
        });
    }

    function resetBtn() {
        if (btnNext) {
            btnNext.disabled = false;
            btnNext.innerHTML =
                '<i class="fa-solid fa-calculator"></i> Hitung Fuzzy-AHP';
        }
    }

    function showErrorToast(msg) {
        var existing = document.getElementById('ahpErrorToast');
        if (existing) existing.remove();

        var toast = document.createElement('div');
        toast.id = 'ahpErrorToast';
        toast.style.cssText =
            'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);'
            + 'background:#ef4444;color:#fff;padding:14px 24px;border-radius:12px;'
            + 'font-size:14px;font-weight:600;box-shadow:0 4px 24px rgba(0,0,0,.2);'
            + 'z-index:9999;max-width:90vw;text-align:center;'
            + 'animation:slideUp .25s ease';
        toast.innerHTML =
            '<i class="fa-solid fa-triangle-exclamation" style="margin-right:8px"></i>' + msg;
        document.body.appendChild(toast);
        setTimeout(function () { if (toast.parentNode) toast.remove(); }, 5000);
    }

    /* ── INIT ── */
    renderStep(true);
});
