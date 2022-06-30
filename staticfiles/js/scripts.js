(() => {
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const confirmed = confirm('Você tem certeza?');
    
            if (confirmed) {
                form.submit();
            }
        })
    }

})();


(() => {
    const buttonClosedMenu = document.querySelector('.button-close-menu');
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const menuContainer = document.querySelector('.menu-container');

    const buttonShowMenuVisibleClass = 'button-show-menu-visible';
    const menuHiddenClass = 'menu-hidden';

    const closeMenu = () => {
        buttonShowMenu.classList.add(buttonShowMenuVisibleClass)
        menuContainer.classList.add(menuHiddenClass)
    }
    
    const showMenu = () => {
        buttonShowMenu.classList.remove(buttonShowMenuVisibleClass)
        menuContainer.classList.remove(menuHiddenClass)
    }

    buttonShowMenu?.addEventListener('click', () => showMenu())
    buttonClosedMenu?.addEventListener('click', () => closeMenu())
    
})();

(() => {
 const authorsLogoutLinks = document.querySelectorAll('.authors-logout-link');
 const formLogout = document.querySelector('.form-logout');

 for (const link of authorsLogoutLinks) {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        formLogout.submit();
    });
 };
})();
