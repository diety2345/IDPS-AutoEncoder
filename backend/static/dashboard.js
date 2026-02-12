setInterval(() => {
    fetch('/alerts')
    .then(res => res.json())
    .then(data => {
        document.getElementById('alertCount').textContent = data.length;
        const table = document.getElementById('alertsTable');
        table.innerHTML = '<tr><th>Time</th><th>Severity</th><th>Score</th></tr>';
        data.slice(-10).forEach(a => {
            const row = table.insertRow();
            row.innerHTML = `<td>${a.time}</td><td class="high">${a.severity}</td><td>${a.score.toFixed(2)}</td>`;
        });
    });
}, 2000);
