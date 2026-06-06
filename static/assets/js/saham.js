/* =========================
   FILE : saham.js
   Search & filter tabel
========================= */

document.addEventListener('DOMContentLoaded', function () {

    /* Terapkan lebar mini-bar dari data-w attribute */
    document.querySelectorAll('.mini-bar[data-w]').forEach(function (el) {
        el.style.width = (el.getAttribute('data-w') || 0) + '%';
    });

    var searchInput  = document.getElementById('searchInput');
    var filterSelect = document.getElementById('filterSelect');
    var table        = document.getElementById('stockTable');

    if (!table) return;

    var EMPTY_ROW_ID = 'emptyFilterRow';

    function filterTable() {
        var q = searchInput  ? searchInput.value.toLowerCase()  : '';
        var f = filterSelect ? filterSelect.value.toLowerCase() : '';
        var tbody = table.querySelector('tbody');
        var visibleCount = 0;

        tbody.querySelectorAll('tr:not(#' + EMPTY_ROW_ID + ')').forEach(function (row) {
            var text = row.textContent.toLowerCase();
            var code = row.cells[0] ? row.cells[0].textContent.toLowerCase() : '';
            var ok   = (!q || text.includes(q)) && (!f || code.includes(f));
            row.style.display = ok ? '' : 'none';
            if (ok) visibleCount++;
        });

        var emptyRow = document.getElementById(EMPTY_ROW_ID);
        if (visibleCount === 0) {
            if (!emptyRow) {
                emptyRow = document.createElement('tr');
                emptyRow.id = EMPTY_ROW_ID;
                var td = document.createElement('td');
                td.colSpan = 99;
                td.style.cssText = 'text-align:center;padding:24px;color:#94a3b8;font-size:14px';
                td.innerHTML = '<i class="fa-solid fa-magnifying-glass" style="margin-right:8px;opacity:.5"></i>'
                    + 'Tidak ada saham yang cocok dengan pencarian.';
                emptyRow.appendChild(td);
                tbody.appendChild(emptyRow);
            } else {
                emptyRow.style.display = '';
            }
        } else if (emptyRow) {
            emptyRow.style.display = 'none';
        }
    }

    if (searchInput)  searchInput.addEventListener('input',  filterTable);
    if (filterSelect) filterSelect.addEventListener('change', filterTable);
});
