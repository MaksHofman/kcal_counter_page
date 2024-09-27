document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('progressChart').getContext('2d');

    const progressData = JSON.parse(document.getElementById('progressData').textContent);
    const progressLabels = JSON.parse(document.getElementById('progressLabels').textContent);

    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: progressLabels,
            datasets: [{
                label: 'Mass Progress',
                data: progressData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
});
