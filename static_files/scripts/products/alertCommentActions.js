function alertDeleteComment(comment_id, product, page, product_pk) {
    Swal.fire({
        title: 'Изтриване на коментар?', showCancelButton: true, cancelButtonText: 'Отказ', confirmButtonText: 'Изтрий',
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/delete-comment/${comment_id}/${product}/${page}/${product_pk}/`;
        }
    });
}

function showOrHideEditCommentForm() {
    const editCommentForm = event.target.parentElement.parentElement.querySelector('form');
    const inputValue = editCommentForm.querySelector('.add-comment-input');

    if (window.getComputedStyle(editCommentForm).opacity === '0') {
        editCommentForm.style.display = 'block';
        setTimeout(() => {
            inputValue.value = editCommentForm.parentElement.querySelector('.comment').textContent;
            editCommentForm.style.opacity = '100%';
        }, 50);
    } else {
        editCommentForm.style.opacity = '0';
        setTimeout(() => {
            editCommentForm.style.display = 'none';
            inputValue.value = editCommentForm.parentElement.querySelector('.comment').textContent;
        }, 350)
    }
}

function validateEditedComment() {
    const editedCommentInputValue = event.target.parentElement.parentElement.querySelector('.add-comment-input');

    if (editedCommentInputValue.value.length < 10) {
        event.preventDefault();

        Swal.fire({
            title: 'Невалиден коментар',
            text: 'Коментарът трябва да съдържа минимум 10 символа',
            icon: 'error',
            confirmButtonText: 'Нов опит',
            confirmButtonColor: '#4d4d4d',
            scrollbarPadding: false
        });
    }
}
