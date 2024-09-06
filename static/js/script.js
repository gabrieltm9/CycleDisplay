let cycle = true;
let cycleTime = 10000;

let pages = ['/', '/stocks', '/news'];
let currentPage = localStorage.getItem('currentPage') || 0;

function showNextPage() {
    currentPage = (currentPage + 1) % pages.length;
    localStorage.setItem('currentPage', currentPage);
    window.location.href = pages[currentPage];
}

function showPreviousPage() {
    currentPage = (currentPage - 1 + pages.length) % pages.length;
    localStorage.setItem('currentPage', currentPage);
    window.location.href = pages[currentPage];
}

// Change page if cycle is enabled 
function cyclePages() {
    if (cycle) {
        showNextPage();
    }
}

setInterval(cyclePages, cycleTime);