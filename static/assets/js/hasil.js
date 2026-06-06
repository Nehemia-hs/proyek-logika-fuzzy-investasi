/* =========================
   FILE : hasil.js
   Hasil Fuzzy-AHP saja
   Requires: comparisonData (injected via Jinja)
========================= */

document.addEventListener('DOMContentLoaded', function () {
    if (typeof comparisonData === 'undefined' || !comparisonData) return;

    var fuzzy = comparisonData.fuzzy;
    var rankF = comparisonData.ranking_fuzzy;
    var C_FUZZY = '#7c3aed';

    function buildRankChart(canvas, ranking, color) {
        var labels = ranking.map(function (s) { return s.kode; });
        var scores = ranking.map(function (s) { return parseFloat(s.skor.toFixed(4)); });
        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: scores,
                    backgroundColor: scores.map(function (_, i) {
                        var alpha = ['.90', '.72', '.56', '.40', '.28'];
                        var hex   = color.replace('#', '');
                        var r     = parseInt(hex.slice(0,2),16);
                        var g     = parseInt(hex.slice(2,4),16);
                        var b     = parseInt(hex.slice(4,6),16);
                        return 'rgba('+r+','+g+','+b+','+(alpha[i]||'.20')+')';
                    }),
                    borderRadius: 8,
                    borderSkipped: false,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (c) { return ' Skor: ' + c.raw.toFixed(4); },
                        },
                        backgroundColor: 'rgba(0,0,0,.8)',
                        titleFont: { size: 13, weight: 'bold' },
                        bodyFont: { size: 12 },
                        padding: 12,
                    },
                },
                scales: {
                    x: {
                        min: 0, max: 1,
                        grid: { color: 'rgba(124,58,237,.08)' },
                        ticks: { font: { size: 12, weight: '500' }, color: '#64748b', callback: function (v) { return v.toFixed(2); }, maxTicksLimit: 6 },
                    },
                    y: {
                        grid: { display: false },
                        ticks: { font: { size: 13, weight: '600' }, color: '#1f2937' },
                    },
                },
            },
        });
    }

    var rankFCanvas = document.getElementById('rankFuzzyChart');
    if (rankFCanvas) buildRankChart(rankFCanvas, rankF, C_FUZZY);

    /* ── Donut chart distribusi bobot ── */
    var bobotCanvas = document.getElementById('bobotChart');
    if (bobotCanvas && fuzzy && fuzzy.bobot) {
        var bobotKeys   = ['return', 'risiko', 'dividend', 'stabilitas'];
        var bobotLabels = ['Return', 'Risiko', 'Dividend', 'Stabilitas'];
        var bobotColors = ['#2563eb', '#ef4444', '#16a34a', '#7c3aed'];
        var bobotVals   = bobotKeys.map(function (k) { return fuzzy.bobot[k] || 0; });

        new Chart(bobotCanvas, {
            type: 'doughnut',
            data: {
                labels: bobotLabels,
                datasets: [{
                    data: bobotVals,
                    backgroundColor: bobotColors,
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverOffset: 8,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (c) {
                                return ' ' + c.label + ': ' + (c.raw * 100).toFixed(2) + '%';
                            },
                        },
                        backgroundColor: 'rgba(0,0,0,.8)',
                        titleFont: { size: 13, weight: 'bold' },
                        bodyFont: { size: 12 },
                        padding: 12,
                    },
                },
            },
        });

        var legendEl = document.getElementById('donutLegend');
        if (legendEl) {
            legendEl.innerHTML = '';
            bobotLabels.forEach(function (lbl, i) {
                legendEl.innerHTML +=
                    '<div class="donut-legend-item">'
                    + '<span class="donut-legend-dot" style="background:' + bobotColors[i] + '"></span>'
                    + '<span class="donut-legend-label">' + lbl + '</span>'
                    + '<span class="donut-legend-val">' + (bobotVals[i] * 100).toFixed(2) + '%</span>'
                    + '</div>';
            });
        }
    }

    /* ── Tabel TFN ── */
    var tfnBody = document.getElementById('tfnTableBody');
    if (tfnBody && fuzzy.bobot_tfn) {
        var keys   = ['return', 'risiko', 'dividend', 'stabilitas'];
        var labels = ['Return', 'Risiko', 'Dividend Yield', 'Stabilitas'];
        keys.forEach(function (k, idx) {
            var t = fuzzy.bobot_tfn[k];
            if (!t) return;
            tfnBody.innerHTML +=
                '<tr>'
                + '<td><strong>' + labels[idx] + '</strong></td>'
                + '<td>' + t.l.toFixed(4) + '</td>'
                + '<td>' + t.m.toFixed(4) + '</td>'
                + '<td>' + t.u.toFixed(4) + '</td>'
                + '<td><span class="tfn-badge">' + fuzzy.bobot[k].toFixed(4) + '</span></td>'
                + '</tr>';
        });
    }
});
