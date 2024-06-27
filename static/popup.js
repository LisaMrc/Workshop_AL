document.addEventListener('DOMContentLoaded', (event) => {

    const popup = document.getElementById('popup');
    const openPopupBtn = document.getElementById('openPopupBtn');
    const closePopupBtn = document.getElementById('closePopupBtn');

    openPopupBtn.onclick = function() {
        popup.style.display = 'block';
    }

    closePopupBtn.onclick = function() {
        popup.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == popup) {
            popup.style.display = 'none';
        }
    }
});