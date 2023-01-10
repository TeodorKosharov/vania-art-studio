window.onbeforeunload = function () {
    localStorage.setItem('scrollpos', window.scrollY);
}

window.onload = function () {
    const scrollPosition = localStorage.getItem('scrollpos');
    if (scrollPosition) {
        window.scrollTo(0, parseFloat(scrollPosition));
    }
}
