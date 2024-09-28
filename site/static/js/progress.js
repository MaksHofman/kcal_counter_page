document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('progressChart').getContext('2d');
    const progressTypeSelect = document.getElementById("progress-type-select");

    const progressTypeLabels = {
        mass: "Mass",
        pr_chest: "Chest PR",
        pr_deadlift: "Deadlift PR",
        pr_squat: "Squat PR",
        fat_percentage: "Body Fat Percentage"
    };

    let myChart;

    function getChartColor(type) {
        switch (type) {
            case 'mass':
                return {
                    background: 'rgba(75, 192, 192, 0.2)',
                    border: 'rgba(75, 192, 192, 1)'
                };
            case 'pr_chest':
                return {
                    background: 'rgba(255, 99, 132, 0.2)',
                    border: 'rgba(255, 99, 132, 1)'
                };
            case 'pr_deadlift':
                return {
                    background: 'rgba(54, 162, 235, 0.2)',
                    border: 'rgba(54, 162, 235, 1)'
                };
            case 'pr_squat':
                return {
                    background: 'rgba(153, 102, 255, 0.2)',
                    border: 'rgba(153, 102, 255, 1)'
                };
            case 'fat_percentage':
                return {
                    background: 'rgba(255, 159, 64, 0.2)',
                    border: 'rgba(255, 159, 64, 1)'
                };
            default:
                return {
                    background: 'rgba(201, 203, 207, 0.2)',
                    border: 'rgba(201, 203, 207, 1)'
                };
        }
    }

    function createChart(type, data, labels) {
        if (myChart) {
            myChart.destroy();
        }

        const color = getChartColor(type);
        const unit = (type==='fat_percentage') ? "%" : "kg";
        const label = progressTypeLabels[type];

        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `${label}`,
                    data: data,
                    backgroundColor: color.background,
                    borderColor: color.border,
                    borderWidth: 2
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
                },
                plugins: {
                    legend: {
                        onClick: (e) => {
                            e.stopPropagation();
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `${label}: ${tooltipItem.raw}${unit}`;
                            },
                            title: function(tooltipItems) {
                                const date = tooltipItems[0].label;
                                return new Date(date).toLocaleDateString('en-GB', {
                                    year: 'numeric',
                                    month: 'short',
                                    day: 'numeric'
                                });
                            }
                        }
                    }
                }
            }
        });
    }

    function fetchProgressData(progressType) {
        fetch(`/progress_data?progress_type=${progressType}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error fetching data: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error('Server error:', data.error);
                    alert('Error fetching progress data. Please try again later.');
                } else {
                    createChart(progressType, data.data, data.labels);
                }
            })
            .catch(error => {
                console.error('Error fetching progress data:', error);
                alert('An error occurred while fetching progress data.');
            });
    }

    fetchProgressData(progressTypeSelect.value);

    progressTypeSelect.addEventListener('change', function() {
        const selectedType = this.value;
        fetchProgressData(selectedType);
    });
});
