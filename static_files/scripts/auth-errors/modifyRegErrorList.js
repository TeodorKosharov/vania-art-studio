const usernameErrPara = document.querySelector('.username-error-message');
const emailErrPara = document.querySelector('.email-error-message');
const passwordErrPara = document.querySelector('.password-error-message');


function modifyRegErrorList() {
    const errorLists = document.querySelectorAll('ul[class="errorlist"]');
    errorLists.forEach(errList => {
        errList.style.display = 'none';
        const error = errList.children[0].textContent;

        if (error.includes('Парола') || error.includes('Пароли')) {
            passwordErrPara.textContent = error;
        } else if (error.includes('email')) {
            emailErrPara.textContent = 'Моля, въведете валиден e-mail адрес';
        } else if (error.includes('име')) {
            usernameErrPara.textContent = error
        }
    });

    if (errorLists.length > 0) {
        document.querySelectorAll('input').forEach(inp => {
            inp.className = 'error-inputs';
        });
    }
}

window.onload = modifyRegErrorList;
