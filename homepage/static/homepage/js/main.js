(function () {
    "use strict";

    const yearElement = document.getElementById("current-year");
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    const navLinks = document.querySelectorAll(".nav-link");
    const currentPath = window.location.pathname;

    navLinks.forEach(function (link) {
        const href = link.getAttribute("href");
        if (!href) return;

        const isRoot = href === "/";
        const matches = isRoot
            ? currentPath === "/"
            : currentPath.startsWith(href);

        if (matches) {
            link.classList.add("fw-bold", "text-primary");
        }
    });
})();
