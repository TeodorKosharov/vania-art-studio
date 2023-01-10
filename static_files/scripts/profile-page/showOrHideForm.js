const form = document.querySelector('.edit-profile-form');
const editProfileTitle = document.querySelector('.edit-profile-title');
const profileTitle = document.querySelector('.profile-title');
const profilePic = document.querySelector('.profile-picture');
const profileInfo = document.querySelector('.profile-info');
const [saveBtn, cancelBtn] = document.querySelectorAll('.action-btn');
const section = document.querySelector('section');
const errorList = document.querySelector('.errorlist');

if (errorList) {
    showOrHideForm();
    errorList.style.display = 'none';
    cancelBtn.disabled = true;
    cancelBtn.style.opacity = '70%';
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


// Hiding the file upload input
const fileInput = document.querySelector('input[type="file"]');
fileInput.style.display = 'none';

saveBtn.addEventListener('click', checkIfFileSelected);

function showOrHideForm() {
    if (window.getComputedStyle(form).display === 'none') {
        profilePic.style.display = 'none';
        profileInfo.style.display = 'none';
        profileTitle.style.display = 'none';
        form.style.display = 'block';
        editProfileTitle.style.display = 'block';
        cancelBtn.style.display = 'block';
        section.style.height = '700px';
    } else {
        form.style.display = 'none';
        editProfileTitle.style.display = 'none';
        cancelBtn.style.display = 'none';
        profileTitle.style.display = 'block';
        profilePic.style.display = 'block';
        profileInfo.style.display = 'block';
        section.style.height = '400px';
    }
}

function checkIfFileSelected(event) {
    if (fileInput.value === '') {
        event.preventDefault();
        Swal.fire({
            title: 'Липсва профилна снимка',
            text: 'Моля, изберете профилна снимка',
            icon: 'error',
            confirmButtonText: 'Нов опит',
            confirmButtonColor: '#4d4d4d',
            scrollbarPadding: false
        })
    } else {
        // window.location.href = '/account/profile';
        console.log(document.querySelector('.errorlist'));
    }
}
