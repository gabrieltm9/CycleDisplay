let cycle = true;
let cycleTime = 10000;

let pages = ['/weather', '/stocks', '/news', '/fifa'];
let currentPage = 0;

function loadPage(page) {
    fetch(page)
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;

            // Remove the previously added script
            var previousScript = document.querySelector('script[data-page]');
            if (previousScript) {
                previousScript.remove();
            }

            // Explicitly delete setContent from the global scope to avoid it persisting between pages
            if (typeof setContent === 'function') {
                delete window.setContent;
            }

            // Load the script for the current page
            var script = document.createElement('script');
            script.src = '/static/js/' + page.split('/')[1] + '.js';
            script.type = 'text/javascript';
            script.setAttribute('data-page', page);
            script.onload = function() {
                // Call setContent() if it's defined in the loaded script
                if (typeof setContent === 'function') {
                    setContent();
                }
            };
            document.body.appendChild(script);
        })
        .catch(err => console.warn('Error loading page: ', err));
}

function showNextPage() {
    currentPage = (currentPage + 1) % pages.length;
    loadPage(pages[currentPage]);
}

function showPreviousPage() {
    currentPage = (currentPage - 1 + pages.length) % pages.length;
    loadPage(pages[currentPage]);
}

// Change page if cycle is enabled 
function cyclePages() {
    if (cycle) {
        showNextPage();
    }
}

window.onload = function() {
    setTimeout(function() {
        loadPage(pages[currentPage]);
        setInterval(cyclePages, cycleTime);
    }, 5000);
}