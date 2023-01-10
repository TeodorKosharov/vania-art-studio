const currentPage = document.querySelector('title').textContent;

document.querySelectorAll('.navi-links').forEach(link => {
    const linkPara = link.querySelector('p');

    if (linkPara.textContent === currentPage) {
        linkPara.parentElement.classList.add('highlight-link');
    } else {
        linkPara.parentElement.classList.remove('highlight-link');
    }
});
