const errorList = document.querySelector('.errorlist');

if (errorList) {
    errorList.style.display = 'none';
    const errorMessage = errorList.querySelector('li').textContent;

    Swal.fire({
        title: 'Невалиден коментар',
        text: errorMessage,
        icon: 'error',
        confirmButtonText: 'Нов опит',
        confirmButtonColor: '#4d4d4d',
        scrollbarPadding: false
    });
}
