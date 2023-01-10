const authLinksContainer = document.querySelector('.auth-links-container');
const profileLogoutLinksContainer = document.querySelector('.profile-logout-links-container');

function showAuthLinksCont() {
    // if querySelector matches logout container then we have to show it, else we show auth links container

    if (profileLogoutLinksContainer !== null) {
        profileLogoutLinksContainer.style.display = 'block';
    } else {
        authLinksContainer.style.display = 'block';
    }
}

function hideAuthLinksCont() {
    // if querySelector matches logout container then we have to hide it, else we hide auth links container

    if (profileLogoutLinksContainer !== null) {
        profileLogoutLinksContainer.style.display = 'none'
    } else {
        authLinksContainer.style.display = 'none';
    }
}
