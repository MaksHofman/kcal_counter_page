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
});
