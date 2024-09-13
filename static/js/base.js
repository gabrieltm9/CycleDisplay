let cycle = true;
let cycleTime = 15000;

let pages = ['/stocks', '/news']; // Removed '/weather'
let currentPage = -1;

// Function to load a page and its associated script
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

// Function to show the next page
function showNextPage() {
    currentPage = (currentPage + 1) % pages.length;
    loadPage(pages[currentPage]);
}

// Function to show the previous page
function showPreviousPage() {
    currentPage = (currentPage - 1 + pages.length) % pages.length;
    loadPage(pages[currentPage]);
}

// Function to show a specific page
window.onload = function() {
    // Check if the current URL is not '/'
    if (window.location.pathname == '/') {
        if (cycle) {
            setTimeout(function() {
                showNextPage();
                    setInterval(showNextPage, cycleTime);
            }, 3000);
        }
    } else {
        document.querySelector('footer').remove();
    }

    setContent();
}

let iconMap = {
    'clear': 'https://basmilius.github.io/weather-icons/production/fill/all/clear-day.svg', 
    'partly-cloudy': 'https://basmilius.github.io/weather-icons/production/fill/all/partly-cloudy-day.svg', 
    'cloudy': 'https://basmilius.github.io/weather-icons/production/fill/all/cloudy.svg', 
    'overcast': 'https://basmilius.github.io/weather-icons/production/fill/all/overcast.svg', 
    'fog': 'https://basmilius.github.io/weather-icons/production/fill/all/fog.svg', 
    'drizzle': 'https://basmilius.github.io/weather-icons/production/fill/all/drizzle.svg', 
    'rain': 'https://basmilius.github.io/weather-icons/production/fill/all/rain.svg', 
    'snow': 'https://basmilius.github.io/weather-icons/production/fill/all/snow.svg', 
    'sleet': 'https://basmilius.github.io/weather-icons/production/fill/all/sleet.svg', 
    'thunderstorms-rain': 'https://basmilius.github.io/weather-icons/production/fill/all/thunderstorms-rain.svg', 
    'thunderstorms-snow': 'https://basmilius.github.io/weather-icons/production/fill/all/thunderstorms-snow.svg', 
    'night-clear': 'https://basmilius.github.io/weather-icons/production/fill/all/clear-night.svg'
};

const weatherCodes = {
    0: { description: "Clear Sky", icon: "clear" },
    1: { description: "Mostly Clear", icon: "clear" },
    2: { description: "Partly Cloudy", icon: "partly-cloudy" },
    3: { description: "Overcast", icon: "overcast" },
    45: { description: "Fog", icon: "fog" },
    48: { description: "Depositing Rime Fog", icon: "fog" },
    51: { description: "Light Drizzle", icon: "drizzle" },
    53: { description: "Moderate Drizzle", icon: "drizzle" },
    55: { description: "Heavy Drizzle", icon: "drizzle" },
    56: { description: "Light Freezing Drizzle", icon: "drizzle" },
    57: { description: "Heavy Freezing Drizzle", icon: "drizzle" },
    61: { description: "Light Rain", icon: "rain" },
    63: { description: "Moderate Rain", icon: "rain" },
    65: { description: "Heavy Rain", icon: "rain" },
    66: { description: "Light Freezing Rain", icon: "rain" },
    67: { description: "Heavy Freezing Rain", icon: "rain" },
    71: { description: "Light Snow", icon: "snow" },
    73: { description: "Moderate Snow", icon: "snow" },
    75: { description: "Heavy Snow", icon: "snow" },
    77: { description: "Snow Grains", icon: "sleet" },
    80: { description: "Light Rain Showers", icon: "rain" },
    81: { description: "Moderate Rain Showers", icon: "rain" },
    82: { description: "Heavy Rain Showers", icon: "rain" },
    85: { description: "Light Snow Showers", icon: "snow" },
    86: { description: "Heavy Snow Showers", icon: "snow" },
    95: { description: "Thunderstorm", icon: "thunderstorms-rain" },
    96: { description: "Thunderstorm with Light Hail", icon: "thunderstorms-snow" },
    99: { description: "Thunderstorm with Heavy Hail", icon: "thunderstorms-snow" },
};

function getWeatherIconURL(weatherCode) {
    const weather = weatherCodes[weatherCode];
    if (!weather) {
        console.warn('Weather code not found:', weatherCode);
        return iconMap['partly-cloudy']; // Default icon
    }
    const iconName = weather.icon;
    return iconMap[iconName] || iconMap['partly-cloudy']; // Fallback to default if icon not found
}

function setContent() {
    const weatherCode = document.getElementById('weather-code').innerText;  
    if (!weatherCode) {
        console.warn("Element 'weather-code' not found!");
        return;
    }

    const weatherIcon = getWeatherIconURL(weatherCode);
    document.getElementById('weather-icon').src = weatherIcon;
    document.getElementById('weather-desc').innerText = weatherCodes[weatherCode].description;
}

window.setContent = setContent;