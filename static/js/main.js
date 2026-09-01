document.addEventListener("DOMContentLoaded", function () {


    /* =====================================================
       PAGE LOADER
    ===================================================== */

    const loader =
        document.querySelector(".page-loader");


    window.addEventListener("load", function () {

        setTimeout(function () {

            if (loader) {

                loader.classList.add("loaded");

            }

        }, 500);

    });


    /* =====================================================
       STICKY NAVIGATION
    ===================================================== */

    const navbar =
        document.querySelector(".navbar");


    function handleScroll() {

        if (!navbar) {
            return;
        }


        if (window.scrollY > 40) {

            navbar.classList.add("scrolled");

        } else {

            navbar.classList.remove("scrolled");

        }

    }


    window.addEventListener(
        "scroll",
        handleScroll,
        { passive: true }
    );


    handleScroll();


    /* =====================================================
       SEARCH PANEL
    ===================================================== */

    const searchToggle =
        document.querySelector(".search-toggle");

    const searchPanel =
        document.querySelector(".search-panel");

    const searchClose =
        document.querySelector(".search-close");

    const searchInput =
        document.querySelector("#site-search");


    function openSearch() {

        if (!searchPanel) {
            return;
        }

        searchPanel.classList.add("active");

        setTimeout(function () {

            if (searchInput) {

                searchInput.focus();

            }

        }, 250);

    }


    function closeSearch() {

        if (!searchPanel) {
            return;
        }

        searchPanel.classList.remove("active");

    }


    if (searchToggle) {

        searchToggle.addEventListener(
            "click",
            openSearch
        );

    }


    if (searchClose) {

        searchClose.addEventListener(
            "click",
            closeSearch
        );

    }


    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {

                closeSearch();

            }

        }
    );


    /* =====================================================
       MOBILE MENU
    ===================================================== */

    const menuToggle =
        document.querySelector(".menu-toggle");

    const navLinks =
        document.querySelector(".nav-links");


    if (menuToggle && navLinks) {

        menuToggle.addEventListener(
            "click",
            function () {

                menuToggle.classList.toggle("active");

                navLinks.classList.toggle(
                    "mobile-open"
                );

            }
        );


        navLinks
            .querySelectorAll("a")
            .forEach(function (link) {

                link.addEventListener(
                    "click",
                    function () {

                        menuToggle.classList.remove(
                            "active"
                        );

                        navLinks.classList.remove(
                            "mobile-open"
                        );

                    }
                );

            });

    }


    /* =====================================================
       BACK TO TOP
    ===================================================== */

    const backToTop =
        document.querySelector(".back-to-top");


    function updateBackToTop() {

        if (!backToTop) {
            return;
        }


        if (window.scrollY > 500) {

            backToTop.classList.add("visible");

        } else {

            backToTop.classList.remove("visible");

        }

    }


    window.addEventListener(
        "scroll",
        updateBackToTop,
        { passive: true }
    );


    updateBackToTop();


    if (backToTop) {

        backToTop.addEventListener(
            "click",
            function () {

                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });

            }
        );

    }


    /* =====================================================
       SCROLL REVEAL
    ===================================================== */

    const revealElements =
        document.querySelectorAll(
            ".category-card, " +
            ".product-card, " +
            ".testimonial, " +
            ".campaign-content, " +
            ".newsletter-inner"
        );


    revealElements.forEach(function (element) {

        element.classList.add("reveal");

    });


    const observer =
        new IntersectionObserver(
            function (entries, observer) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "revealed"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.12
            }
        );


    revealElements.forEach(function (element) {

        observer.observe(element);

    });


    /* =====================================================
       NEWSLETTER
    ===================================================== */

    const newsletterForm =
        document.querySelector(
            ".newsletter-form"
        );


    if (newsletterForm) {

        newsletterForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const emailInput =
                    newsletterForm.querySelector(
                        "input[type='email']"
                    );


                if (!emailInput) {
                    return;
                }


                const email =
                    emailInput.value.trim();


                if (!email) {

                    alert(
                        "Please enter your email address."
                    );

                    emailInput.focus();

                    return;

                }


                if (!email.includes("@")) {

                    alert(
                        "Please enter a valid email address."
                    );

                    emailInput.focus();

                    return;

                }


                alert(
                    "Thank you for joining the UrbanWear community!"
                );


                newsletterForm.reset();

            }
        );

    }


    /* =====================================================
       CART COUNT DEMO
    ===================================================== */

    const cartCount =
        document.querySelector(".cart-count");


    let cartItems =
        Number(
            localStorage.getItem(
                "urbanwear_cart_count"
            )
        ) || 0;


    function updateCartCount() {

        if (!cartCount) {
            return;
        }

        cartCount.textContent =
            cartItems;

    }


    updateCartCount();


    /* =====================================================
       CART BUTTON
    ===================================================== */

    const cartButton =
        document.querySelector(".cart-button");


    if (cartButton) {

        cartButton.addEventListener(
            "click",
            function () {

                alert(
                    "Your shopping cart will be available here soon."
                );

            }
        );

    }


        /* =====================================================
       COLLECTION FILTER ACCORDIONS
    ===================================================== */

    const filterTitles =
        document.querySelectorAll(".filter-title");


    filterTitles.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const group =
                    button.closest(".filter-group");


                if (!group) {
                    return;
                }


                group.classList.toggle("open");

            }
        );

    });


    /* =====================================================
       MOBILE FILTER
    ===================================================== */

    const filterToggle =
        document.querySelector("#filter-toggle");

    const filterSidebar =
        document.querySelector("#filter-sidebar");


    if (filterToggle && filterSidebar) {

        filterToggle.addEventListener(
            "click",
            function () {

                filterSidebar.classList.toggle(
                    "mobile-open"
                );

            }
        );

    }

        /* =====================================================
       PRODUCT SIZE SELECTION
    ===================================================== */

    const sizeButtons =
        document.querySelectorAll(".size-button");


    sizeButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                sizeButtons.forEach(
                    function (item) {

                        item.classList.remove(
                            "selected"
                        );

                    }
                );


                button.classList.add(
                    "selected"
                );

            }
        );

    });


    /* =====================================================
       PRODUCT QUANTITY
    ===================================================== */

    const quantityInput =
        document.querySelector("#product-quantity");

    const quantityMinus =
        document.querySelector(".quantity-minus");

    const quantityPlus =
        document.querySelector(".quantity-plus");


    if (
        quantityInput &&
        quantityMinus &&
        quantityPlus
    ) {

        quantityMinus.addEventListener(
            "click",
            function () {

                let quantity =
                    parseInt(
                        quantityInput.value
                    ) || 1;


                if (quantity > 1) {

                    quantityInput.value =
                        quantity - 1;

                }

            }
        );


        quantityPlus.addEventListener(
            "click",
            function () {

                let quantity =
                    parseInt(
                        quantityInput.value
                    ) || 1;

                const max =
                    parseInt(
                        quantityInput.max
                    ) || 999;


                if (quantity < max) {

                    quantityInput.value =
                        quantity + 1;

                }

            }
        );

    }


    /* =====================================================
       SIZE GUIDE
    ===================================================== */

    const sizeGuideOpen =
        document.querySelector(
            ".size-guide-open"
        );

    const sizeGuideModal =
        document.querySelector(
            "#size-guide-modal"
        );

    const sizeGuideClose =
        document.querySelector(
            ".size-guide-close"
        );

    const sizeGuideOverlay =
        document.querySelector(
            ".size-guide-overlay"
        );


    if (
        sizeGuideOpen &&
        sizeGuideModal
    ) {

        sizeGuideOpen.addEventListener(
            "click",
            function () {

                sizeGuideModal.classList.add(
                    "active"
                );

                document.body.style.overflow =
                    "hidden";

            }
        );

    }


    function closeSizeGuide() {

        if (!sizeGuideModal) {
            return;
        }


        sizeGuideModal.classList.remove(
            "active"
        );

        document.body.style.overflow =
            "";

    }


    if (sizeGuideClose) {

        sizeGuideClose.addEventListener(
            "click",
            closeSizeGuide
        );

    }


    if (sizeGuideOverlay) {

        sizeGuideOverlay.addEventListener(
            "click",
            closeSizeGuide
        );

    }


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape"
            ) {

                closeSizeGuide();

            }

        }
    );

        /* =====================================================
       CART QUANTITY SYNC
    ===================================================== */

    const productQuantity =
        document.querySelector(
            "#product-quantity"
        );

    const cartQuantity =
        document.querySelector(
            "#cart-quantity"
        );


    if (
        productQuantity &&
        cartQuantity
    ) {

        productQuantity.addEventListener(
            "input",
            function () {

                cartQuantity.value =
                    productQuantity.value;

            }
        );

    }


    /* =====================================================
       SELECTED SIZE SYNC
    ===================================================== */

    const selectedSize =
        document.querySelector(
            "#selected-size"
        );


    if (
        selectedSize &&
        sizeButtons.length
    ) {

        sizeButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        selectedSize.value =
                            button.dataset.size;

                    }
                );

            }
        );

    }


});