const filterForm = document.querySelector('.filter-form-container');

function showOrHideFilterForm() {
    if (window.getComputedStyle(filterForm).opacity === '0') {
        filterForm.style.display = 'block';
        setTimeout(() => {
            filterForm.style.opacity = '1';
        }, 50);
    } else {
        filterForm.style.opacity = '0';
        setTimeout(() => {
            filterForm.style.display = 'none';
        }, 350)
    }
}