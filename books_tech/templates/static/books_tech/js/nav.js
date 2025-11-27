(function(){
    // Mobile nav toggle
    const toggle = document.getElementById('nav-toggle');
    const links = document.getElementById('nav-links');
    const nav = document.getElementById('site-nav');

    if (toggle && links) {
        toggle.addEventListener('click', function(){
            const open = links.classList.toggle('open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });

        // Close the menu when clicking a link (mobile)
        links.addEventListener('click', function(e){
            if(e.target.tagName === 'A') {
                links.classList.remove('open');
                toggle.setAttribute('aria-expanded','false');
            }
        });

        // Close menu on resize to desktop
        window.addEventListener('resize', function(){
            if (window.innerWidth > 760) {
                links.classList.remove('open');
                toggle.setAttribute('aria-expanded','false');
            }
        });
    }

    // Add scrolled class when page is scrolled
    function onScroll(){
        if(!nav) return;
        if(window.scrollY > 10) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    }
    window.addEventListener('scroll', onScroll);
    // run once
    onScroll();
})();
