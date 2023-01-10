const addCommentForm = document.querySelector('.add-comment-container');
const showCommentFormBtn = document.querySelector('.add-comment-button');

function showOrHideAddCommentForm() {
    if (window.getComputedStyle(addCommentForm).opacity === '0') {
        addCommentForm.style.display = 'block';
        showCommentFormBtn.textContent = 'Откажи коментар';
        setTimeout(() => {
            addCommentForm.style.opacity = '100%';
        }, 50);
    } else {
        addCommentForm.style.opacity = '0';
        showCommentFormBtn.textContent = 'Добави коментар';
        setTimeout(() => {
            addCommentForm.style.display = 'none';
        }, 350)
    }
}
