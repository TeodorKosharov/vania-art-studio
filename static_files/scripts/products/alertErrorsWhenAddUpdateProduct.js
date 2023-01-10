const errorList = document.querySelector('.errorlist');
const fileInput = document.querySelector('input[type="file"]');
fileInput.style.opacity = '0%';
fileInput.className = 'file-input';

if (errorList) {
    errorList.style.display = 'none';
    let errorsHtml = document.createElement('ul');
    const errors = errorList.querySelectorAll('li');

    for (let index = 0; index < errors.length; index++) {
        if (index % 2 === 1) {
            const liEl = document.createElement('li');
            liEl.textContent = errors[index].textContent;
            errorsHtml.append(liEl);
        }
    }

    Swal.fire({
        title: 'Невалидни стойности',
        html: errorsHtml,
        icon: 'error',
        confirmButtonText: 'Нов опит',
        confirmButtonColor: '#4d4d4d',
        scrollbarPadding: false
    });
}
