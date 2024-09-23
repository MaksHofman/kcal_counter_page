document.addEventListener('DOMContentLoaded', function() {

    // Goal Adjustment Modal
    const modal = document.getElementById('goal-modal');
    const btn = document.getElementById('adj-btn');
    const span = document.querySelector('.modal-content .close-btn');

    btn.onclick = function() {
        modal.style.display = 'block';
    }


    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }

    // Delete Record buttons
    document.querySelectorAll('.delete-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const entryId = this.getAttribute('data-entry-id');
            const confirmDelete = confirm("Are you sure you want to delete this record?");

            if(confirmDelete) {
                fetch(`/delete_calories/${entryId}`, {
                    method: 'POST'
                }).then(response => {
                    if(response.ok) {
                        location.reload();
                    } else {
                        alert('Failed to delete the record. Please try again.')
                    }
                }).catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    });

    // Calories Graph
    let caloriesToday = parseInt(document.getElementById('calories').value);
    let caloricGoal = parseInt(document.getElementById('goal').value);

    const showTooltip = !isNaN(caloricGoal);
    if (isNaN(caloricGoal)) {
        caloricGoal = 1;
        caloriesToday = 0;
    }

    const remainingCalories = caloricGoal - caloriesToday >= 0 ? caloricGoal - caloriesToday : 0;

    const ctx = document.getElementById('calories-chart').getContext('2d');
    const caloriesChart = new Chart(ctx , {
        type: 'doughnut',
        data: {
            labels: ['Calories Consumed', 'Remaining Calories'],
            datasets: [{
                data: [caloriesToday, remainingCalories],
                backgroundColor: ['#d3b03e', '#0f3057'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: showTooltip
                }
            }
        }
    });
});
