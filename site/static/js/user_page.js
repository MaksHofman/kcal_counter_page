document.addEventListener('DOMContentLoaded', function() {
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
});
