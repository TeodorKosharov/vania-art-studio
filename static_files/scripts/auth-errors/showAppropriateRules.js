function showRules(typeRules) {
    document.querySelector(`.${typeRules}-rules`).style.opacity = '1';
}

function hideRules(typeRules) {
    document.querySelector(`.${typeRules}-rules`).style.opacity = '0';
}
