/* =========================
   FILE : dashboard.js
   Chart tren harga saham
========================= */

// Helper: convert hex to rgba
function hexToRgba(hex, alpha) {
    var r = parseInt(hex.slice(1,3), 16);
    var g = parseInt(hex.slice(3,5), 16);
    var b = parseInt(hex.slice(5,7), 16);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
}

document.addEventListener('DOMContentLoaded', function () {

    /* ── TREN CHART ── */
    var trenCanvas = document.getElementById('stockChart');
    if (trenCanvas) {

        var dsColors = ['#2563eb','#10b981','#f59e0b','#ef4444','#8b5cf6'];
        var dashes   = [[],[5,0],[4,2],[2,2],[6,2]];
        var labels   = [];
        var datasets = [];

        if (typeof dashboardStocks !== 'undefined' && dashboardStocks.length) {
            var firstWithHistory = dashboardStocks.find(function (s) {
                return Array.isArray(s.history_values) && s.history_values.length && Array.isArray(s.history_dates) && s.history_dates.length;
            });

            if (firstWithHistory) {
                labels = firstWithHistory.history_dates;
                dashboardStocks.forEach(function (stock, i) {
                    var color = dsColors[i % dsColors.length];
                    datasets.push({
                        label: stock.kode,
                        data: Array.isArray(stock.history_values) ? stock.history_values : [],
                        borderColor: color,
                        backgroundColor: hexToRgba(color, 0.08),
                        borderWidth: 2.5,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: color,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 6,
                        fill: true,
                        borderDash: dashes[i % dashes.length],
                    });
                });
            }
        }

        if (!datasets.length) {
            var wrapper = trenCanvas.parentElement;
            if (wrapper) {
                trenCanvas.style.display = 'none';
                var emptyEl = document.createElement('div');
                emptyEl.style.cssText = 'padding:40px 20px;text-align:center;color:#94a3b8';
                emptyEl.innerHTML =
                    '<i class="fa-solid fa-chart-line" style="font-size:32px;margin-bottom:12px;display:block;opacity:.4"></i>'
                    + '<p style="font-size:14px;font-weight:600;margin:0 0 6px;color:#64748b">Data tren tidak tersedia</p>'
                    + '<p style="font-size:13px;margin:0">Data historis belum berhasil dimuat dari Yahoo Finance.<br>'
                    + 'Coba klik <strong>Refresh</strong> untuk memperbarui.</p>';
                wrapper.appendChild(emptyEl);
            }
            return;
        }

        var seriesLabels = datasets.map(function (series) { return series.label; });

        /* Build legend */
        var legendEl = document.getElementById('chartLegend');
        if (legendEl) {
            legendEl.innerHTML = '';
            seriesLabels.forEach(function (label, i) {
                var s = document.createElement('span');
                s.className = 'legend-item';
                s.style.display = 'inline-flex';
                s.style.alignItems = 'center';
                s.style.marginRight = '16px';
                s.style.marginBottom = '8px';
                s.style.fontSize = '13px';
                s.style.fontWeight = '500';
                s.innerHTML = '<span class="legend-dot" style="background:' + dsColors[i % dsColors.length] + '; width:8px; height:8px; border-radius:50%; margin-right:6px; display:inline-block"></span>' + label;
                legendEl.appendChild(s);
            });
        }

        if (typeof Chart === 'undefined') {
            console.error('Chart.js tidak ditemukan. Pastikan script Chart.js dimuat sebelum dashboard.js');
            return;
        }

        try {
            new Chart(trenCanvas, {
                type: 'line',
                data: { 
                    labels: labels, 
                    datasets: datasets 
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: { 
                        legend: { display: false },
                        filler: { propagate: true },
                        tooltip: { 
                            backgroundColor: 'rgba(0,0,0,.8)',
                            titleFont: { size: 13, weight: 'bold' },
                            bodyFont: { size: 12 },
                            padding: 12,
                            displayColors: true,
                            boxPadding: 6,
                        }
                    },
                    scales: {
                        x: { 
                            grid: { color: 'rgba(47,85,164,.05)', drawBorder: false }, 
                            ticks: { 
                                font: { size: 12, weight: '500' }, 
                                color: '#64748b', 
                                maxRotation: 45, 
                                minRotation: 0,
                                autoSkip: true,
                                maxTicksLimit: 12
                            }
                        },
                        y: { 
                            beginAtZero: false,
                            grid: { color: 'rgba(47,85,164,.08)', drawBorder: false }, 
                            ticks: { 
                                font: { size: 12, weight: '500' }, 
                                color: '#64748b', 
                                callback: function(v) { return v.toLocaleString('id-ID'); },
                                maxTicksLimit: 8
                            }
                        },
                    },
                },
            });
            console.log('✓ Chart rendered successfully with', datasets.length, 'datasets');
        } catch (err) {
            console.error('Dashboard chart error:', err);
            var chartParent = trenCanvas.parentElement;
            if (chartParent) {
                var errorEl = document.createElement('div');
                errorEl.style.padding = '20px';
                errorEl.style.color = '#ef4444';
                errorEl.style.textAlign = 'center';
                errorEl.textContent = 'Grafik tidak dapat ditampilkan saat ini. Silakan refresh halaman.';
                chartParent.appendChild(errorEl);
            }
        }
    }

    /* ── SMOOTH SCROLL + ACTIVE NAV ── */
    document.querySelectorAll('.nav-scroll').forEach(function (a) {
        a.addEventListener('click', function (e) {
            var href = this.getAttribute('href');
            if (href && href[0] === '#') {
                e.preventDefault();
                var t = document.querySelector(href);
                if (t) t.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    var secs = document.querySelectorAll('section[id]');
    var nls  = document.querySelectorAll('.nav-scroll');

    window.addEventListener('scroll', function () {
        var cur = '';
        secs.forEach(function (s) {
            if (window.scrollY >= s.offsetTop - 120) cur = s.id;
        });
        nls.forEach(function (a) {
            a.classList.remove('active');
            if (a.getAttribute('href') === '#' + cur) a.classList.add('active');
        });
    });
});
