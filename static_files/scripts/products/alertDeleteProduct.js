function askForDeletion(product, pk) {
    Swal.fire({
        title: 'Изтриване на продукта?',
        text: 'Промените са необратими!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Изтриване',
        cancelButtonText: 'Отказ'
    });

    document.querySelector('.swal2-confirm').style.backgroundColor = '#555C66';

    document.querySelector('.swal2-confirm').addEventListener('click', () => {
        window.location.href = `/delete/${product}/${pk}/`;
    });
}
