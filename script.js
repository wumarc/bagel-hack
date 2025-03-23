// Navbar title click redirect to index.html
document.addEventListener('DOMContentLoaded', function() {
    const eventTitle = document.getElementById('navTitle');
    
    if (eventTitle) {
        eventTitle.style.cursor = 'pointer';
        eventTitle.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
});
