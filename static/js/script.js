let pages = ['/', '/stocks', '/news'];
let currentPage = 0;

function showNextPage() {
    currentPage = (currentPage + 1) % pages.length;
    window.location.href = pages[currentPage];
}

function showPreviousPage() {
    currentPage = (currentPage - 1 + pages.length) % pages.length;
    window.location.href = pages[currentPage];
}

// Automatically change page every 10 seconds
setInterval(showNextPage, 10000);

// You can call showNextPage() and showPreviousPage() from external events if needed
