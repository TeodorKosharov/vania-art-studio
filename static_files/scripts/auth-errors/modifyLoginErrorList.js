function modifyLoginErrorList() {
    const errorList = document.querySelector('.errorlist');
    if (errorList) {
        errorList.style.display = 'none';
        const error = errorList.children[0].textContent.replace('__all__', '');
        document.querySelector('.error-message').textContent = error;
        document.querySelectorAll('input').forEach(inp => {
            if (inp.type !== 'hidden') {
                inp.className = 'error-inputs';
                inp.value = '';
            }
        });
    }
}

window.onload = modifyLoginErrorList;
