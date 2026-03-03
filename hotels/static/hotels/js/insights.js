document.addEventListener('DOMContentLoaded', () => {
    // Revenue Chart
    const ctx1 = document.getElementById('propChart')?.getContext('2d');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'doughnut',
            data: {
                labels: ['Room Revenue', 'F&B', 'Services', 'Events'],
                datasets: [{
                    data: [65, 20, 10, 5],
                    backgroundColor: ['#d4af37', '#06b6d4', '#22c55e', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } },
                maintainAspectRatio: false
            }
        });
    }

    // Demographics Chart
    const ctx2 = document.getElementById('demoChart')?.getContext('2d');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: ['Business', 'Leisure', 'Families', 'Solo'],
                datasets: [{
                    label: '% of Guests',
                    data: [40, 35, 15, 10],
                    backgroundColor: '#06b6d4',
                    borderRadius: 8
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                },
                plugins: { legend: { display: false } },
                maintainAspectRatio: false
            }
        });
    }
});
