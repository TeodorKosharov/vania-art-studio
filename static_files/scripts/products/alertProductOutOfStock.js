document.querySelectorAll('.out-of-stock').forEach(anchor => {
    anchor.parentElement.addEventListener('click', () => {
        Swal.fire({
            icon: 'error', title: 'Продуктът не е в наличност', text: 'Очаквайте зареждане!',
        });
        document.querySelector('.swal2-confirm').style.backgroundColor = '#555C66';
    });
});
