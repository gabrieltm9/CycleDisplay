// Weather icon mapping (same as base.js)
const weatherCodeMap = {
    0: { icon: 'clear-day.svg', desc: 'Clear' },
    1: { icon: 'partly-cloudy-day.svg', desc: 'Mainly Clear' },
    2: { icon: 'partly-cloudy-day.svg', desc: 'Partly Cloudy' },
    3: { icon: 'cloudy.svg', desc: 'Overcast' },
    45: { icon: 'fog.svg', desc: 'Foggy' },
    48: { icon: 'fog.svg', desc: 'Rime Fog' },
    51: { icon: 'drizzle.svg', desc: 'Light Drizzle' },
    53: { icon: 'drizzle.svg', desc: 'Moderate Drizzle' },
    55: { icon: 'drizzle.svg', desc: 'Dense Drizzle' },
    56: { icon: 'sleet.svg', desc: 'Light Freezing Drizzle' },
    57: { icon: 'sleet.svg', desc: 'Dense Freezing Drizzle' },
    61: { icon: 'rain.svg', desc: 'Slight Rain' },
    63: { icon: 'rain.svg', desc: 'Moderate Rain' },
    65: { icon: 'rain.svg', desc: 'Heavy Rain' },
    66: { icon: 'sleet.svg', desc: 'Light Freezing Rain' },
    67: { icon: 'sleet.svg', desc: 'Heavy Freezing Rain' },
    71: { icon: 'snow.svg', desc: 'Slight Snow' },
    73: { icon: 'snow.svg', desc: 'Moderate Snow' },
    75: { icon: 'snow.svg', desc: 'Heavy Snow' },
    77: { icon: 'hail.svg', desc: 'Snow Grains' },
    80: { icon: 'rain.svg', desc: 'Slight Rain Showers' },
    81: { icon: 'rain.svg', desc: 'Moderate Rain Showers' },
    82: { icon: 'rain.svg', desc: 'Violent Rain Showers' },
    85: { icon: 'snow.svg', desc: 'Slight Snow Showers' },
    86: { icon: 'snow.svg', desc: 'Heavy Snow Showers' },
    95: { icon: 'thunderstorms.svg', desc: 'Thunderstorm' },
    96: { icon: 'thunderstorms-rain.svg', desc: 'Thunderstorm with Slight Hail' },
    99: { icon: 'thunderstorms-rain.svg', desc: 'Thunderstorm with Heavy Hail' }
};

// Initialize weather icons
function initWeatherIcons() {
    const weatherDays = document.querySelectorAll('.weather-day');
    
    weatherDays.forEach(day => {
        const code = parseInt(day.getAttribute('data-code'));
        const iconElement = day.querySelector('.weather-icon');
        
        if (weatherCodeMap[code]) {
            const iconPath = `https://basmilius.github.io/weather-icons/production/fill/all/${weatherCodeMap[code].icon}`;
            iconElement.src = iconPath;
            iconElement.alt = weatherCodeMap[code].desc;
        }
    });
}

// News Carousel
class NewsCarousel {
    constructor() {
        this.track = document.querySelector('.carousel-track');
        this.dotsContainer = document.querySelector('.carousel-dots');
        
        // Check if elements exist before proceeding
        if (!this.track || !this.dotsContainer) return;
        
        this.cards = document.querySelectorAll('.news-card');
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        this.autoPlayDelay = 5000; // 5 seconds
        
        this.init();
    }
    
    init() {
        if (this.cards.length === 0) return;
        
        this.createDots();
        this.startAutoPlay();
        this.addEventListeners();
    }
    
    createDots() {
        this.cards.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.classList.add('carousel-dot');
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => this.goToSlide(index));
            this.dotsContainer.appendChild(dot);
        });
        this.dots = document.querySelectorAll('.carousel-dot');
    }
    
    goToSlide(index) {
        this.currentIndex = index;
        this.updateCarousel();
        this.resetAutoPlay();
    }
    
    nextSlide() {
        this.currentIndex = (this.currentIndex + 1) % this.cards.length;
        this.updateCarousel();
    }
    
    prevSlide() {
        this.currentIndex = (this.currentIndex - 1 + this.cards.length) % this.cards.length;
        this.updateCarousel();
    }
    
    updateCarousel() {
        const offset = -this.currentIndex * 100;
        this.track.style.transform = `translateX(${offset}%)`;
        
        // Update dots
        this.dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }
    
    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => {
            this.nextSlide();
        }, this.autoPlayDelay);
    }
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    resetAutoPlay() {
        this.stopAutoPlay();
        this.startAutoPlay();
    }
    
    addEventListeners() {
        // Pause on hover
        const newsCarousel = document.querySelector('.news-carousel');
        newsCarousel.addEventListener('mouseenter', () => this.stopAutoPlay());
        newsCarousel.addEventListener('mouseleave', () => this.startAutoPlay());
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                this.prevSlide();
                this.resetAutoPlay();
            } else if (e.key === 'ArrowRight') {
                this.nextSlide();
                this.resetAutoPlay();
            }
        });
        
        // Touch/swipe support
        let touchStartX = 0;
        let touchEndX = 0;
        
        this.track.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            this.stopAutoPlay();
        });
        
        this.track.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe();
            this.startAutoPlay();
        });
        
        this.handleSwipe = () => {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    this.nextSlide();
                } else {
                    this.prevSlide();
                }
            }
        };
    }
}

// Footer weather icon setup
const footerWeatherCodes = {
    0: { description: "Clear Sky", icon: "clear-day.svg" },
    1: { description: "Mostly Clear", icon: "clear-day.svg" },
    2: { description: "Partly Cloudy", icon: "partly-cloudy-day.svg" },
    3: { description: "Overcast", icon: "overcast.svg" },
    45: { description: "Fog", icon: "fog.svg" },
    48: { description: "Depositing Rime Fog", icon: "fog.svg" },
    51: { description: "Light Drizzle", icon: "drizzle.svg" },
    53: { description: "Moderate Drizzle", icon: "drizzle.svg" },
    55: { description: "Heavy Drizzle", icon: "drizzle.svg" },
    56: { description: "Light Freezing Drizzle", icon: "drizzle.svg" },
    57: { description: "Heavy Freezing Drizzle", icon: "drizzle.svg" },
    61: { description: "Light Rain", icon: "rain.svg" },
    63: { description: "Moderate Rain", icon: "rain.svg" },
    65: { description: "Heavy Rain", icon: "rain.svg" },
    66: { description: "Light Freezing Rain", icon: "rain.svg" },
    67: { description: "Heavy Freezing Rain", icon: "rain.svg" },
    71: { description: "Light Snow", icon: "snow.svg" },
    73: { description: "Moderate Snow", icon: "snow.svg" },
    75: { description: "Heavy Snow", icon: "snow.svg" },
    77: { description: "Snow Grains", icon: "sleet.svg" },
    80: { description: "Light Rain Showers", icon: "rain.svg" },
    81: { description: "Moderate Rain Showers", icon: "rain.svg" },
    82: { description: "Heavy Rain Showers", icon: "rain.svg" },
    85: { description: "Light Snow Showers", icon: "snow.svg" },
    86: { description: "Heavy Snow Showers", icon: "snow.svg" },
    95: { description: "Thunderstorm", icon: "thunderstorms.svg" },
    96: { description: "Thunderstorm with Light Hail", icon: "thunderstorms-rain.svg" },
    99: { description: "Thunderstorm with Heavy Hail", icon: "thunderstorms-rain.svg" },
};

function initFooterWeather() {
    const weatherCodeElem = document.getElementById('weather-code');
    if (!weatherCodeElem) return;
    
    const weatherCode = parseInt(weatherCodeElem.textContent.trim());
    const weatherInfo = footerWeatherCodes[weatherCode];
    
    if (weatherInfo) {
        const weatherIcon = document.getElementById('weather-icon');
        const weatherDesc = document.getElementById('weather-desc');
        
        if (weatherIcon) {
            weatherIcon.src = `https://basmilius.github.io/weather-icons/production/fill/all/${weatherInfo.icon}`;
        }
        if (weatherDesc) {
            weatherDesc.textContent = weatherInfo.description;
        }
    }
}

// Dark Mode Management based on Sunset/Sunrise times
function checkDarkMode() {
    const sunriseElem = document.getElementById('sunrise');
    const sunsetElem = document.getElementById('sunset');
    
    if (!sunriseElem || !sunsetElem) {
        // Fallback to hardcoded times if elements not found
        const now = new Date();
        const hours = now.getHours();
        const isDarkModeTime = hours >= 22 || hours < 9;
        
        if (isDarkModeTime) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
        return;
    }
    
    // Parse sunrise and sunset times (format: "HH:MM AM/PM")
    const sunriseText = sunriseElem.textContent.trim();
    const sunsetText = sunsetElem.textContent.trim();
    
    const sunriseTime = parseTime(sunriseText);
    const sunsetTime = parseTime(sunsetText);
    
    if (sunriseTime === null || sunsetTime === null) {
        console.warn('Could not parse sunrise/sunset times');
        return;
    }
    
    const now = new Date();
    const currentTime = now.getHours() * 60 + now.getMinutes(); // Current time in minutes
    
    // Dark mode is active if current time is after sunset OR before sunrise
    const isDarkModeTime = currentTime >= sunsetTime || currentTime < sunriseTime;
    
    if (isDarkModeTime) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}

// Helper function to parse time string in "HH:MM AM/PM" format to minutes since midnight
function parseTime(timeStr) {
    const match = timeStr.match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i);
    if (!match) return null;
    
    let hours = parseInt(match[1]);
    const minutes = parseInt(match[2]);
    const period = match[3].toUpperCase();
    
    // Convert to 24-hour format
    if (period === 'PM' && hours !== 12) {
        hours += 12;
    } else if (period === 'AM' && hours === 12) {
        hours = 0;
    }
    
    return hours * 60 + minutes; // Return total minutes since midnight
}

// Auto-refresh page after 5 minutes to trigger data update
function setupAutoRefresh() {
    const refreshInterval = 5 * 60 * 1000; // 5 minutes in milliseconds
    
    setTimeout(() => {
        console.log('Auto-refreshing page to fetch updated data...');
        window.location.reload();
    }, refreshInterval);
}

// Randomized Gradient Background
function initRandomizedGradient() {
    const body = document.body;
    
    // Add CSS for smooth transitions of CSS variables
    const style = document.createElement('style');
    style.textContent = `
        body {
            transition: 
                --grad1-x 8s ease-in-out,
                --grad1-y 8s ease-in-out,
                --grad2-x 10s ease-in-out,
                --grad2-y 10s ease-in-out,
                --grad3-x 9s ease-in-out,
                --grad3-y 9s ease-in-out,
                --grad4-x 11s ease-in-out,
                --grad4-y 11s ease-in-out,
                --grad5-x 7s ease-in-out,
                --grad5-y 7s ease-in-out,
                --grad6-x 9s ease-in-out,
                --grad6-y 9s ease-in-out,
                --grad7-x 10s ease-in-out,
                --grad7-y 10s ease-in-out;
        }
        @property --grad1-x { syntax: '<percentage>'; inherits: true; initial-value: 15%; }
        @property --grad1-y { syntax: '<percentage>'; inherits: true; initial-value: 25%; }
        @property --grad2-x { syntax: '<percentage>'; inherits: true; initial-value: 75%; }
        @property --grad2-y { syntax: '<percentage>'; inherits: true; initial-value: 65%; }
        @property --grad3-x { syntax: '<percentage>'; inherits: true; initial-value: 45%; }
        @property --grad3-y { syntax: '<percentage>'; inherits: true; initial-value: 55%; }
        @property --grad4-x { syntax: '<percentage>'; inherits: true; initial-value: 85%; }
        @property --grad4-y { syntax: '<percentage>'; inherits: true; initial-value: 15%; }
        @property --grad5-x { syntax: '<percentage>'; inherits: true; initial-value: 5%; }
        @property --grad5-y { syntax: '<percentage>'; inherits: true; initial-value: 75%; }
        @property --grad6-x { syntax: '<percentage>'; inherits: true; initial-value: 60%; }
        @property --grad6-y { syntax: '<percentage>'; inherits: true; initial-value: 35%; }
        @property --grad7-x { syntax: '<percentage>'; inherits: true; initial-value: 25%; }
        @property --grad7-y { syntax: '<percentage>'; inherits: true; initial-value: 85%; }
    `;
    document.head.appendChild(style);
    
    // Function to generate random percentage between min and max
    function randomPercent(min = 0, max = 100) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    // Function to update gradient positions with smooth transition
    function updateGradientPositions() {
        for (let i = 1; i <= 7; i++) {
            body.style.setProperty(`--grad${i}-x`, randomPercent(0, 100) + '%');
            body.style.setProperty(`--grad${i}-y`, randomPercent(0, 100) + '%');
        }
    }
    
    // Initial setup
    updateGradientPositions();
    
    // Update gradient positions every 8-12 seconds for smooth organic flow
    setInterval(updateGradientPositions, Math.random() * 4000 + 8000);
}

// Auto-refresh page after 5 minutes to trigger data update
function setupAutoRefresh() {
    const refreshInterval = 5 * 60 * 1000; // 5 minutes in milliseconds
    
    setTimeout(() => {
        console.log('Auto-refreshing page to fetch updated data...');
        window.location.reload();
    }, refreshInterval);
}

// Tile Swapper for Watchlist and Subway
class TileSwapper {
    constructor() {
        this.tiles = document.querySelectorAll('.swappable-tile');
        this.currentIndex = 0;
        this.swapInterval = 30000; // 30 seconds
        this.autoSwapTimer = null;
        
        if (this.tiles.length > 1) {
            this.init();
        }
    }
    
    init() {
        this.startAutoSwap();
    }
    
    swap() {
        // Remove active class from current tile
        this.tiles[this.currentIndex].classList.remove('active');
        
        // Move to next tile
        this.currentIndex = (this.currentIndex + 1) % this.tiles.length;
        
        // Add active class to new tile
        this.tiles[this.currentIndex].classList.add('active');
    }
    
    startAutoSwap() {
        this.autoSwapTimer = setInterval(() => {
            this.swap();
        }, this.swapInterval);
    }
    
    stopAutoSwap() {
        if (this.autoSwapTimer) {
            clearInterval(this.autoSwapTimer);
            this.autoSwapTimer = null;
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initWeatherIcons();
    initFooterWeather();
    new NewsCarousel();
    new TileSwapper();
    
    // Check dark mode immediately
    checkDarkMode();
    
    // Check dark mode every minute
    setInterval(checkDarkMode, 60000);
    
    // Setup auto-refresh after 5 minutes
    setupAutoRefresh();
    
    // Initialize randomized gradient background
    initRandomizedGradient();
    
    // Update clock in real-time
    updateClock();
    setInterval(updateClock, 1000);
});

// Function to update the clock in real-time
function updateClock() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 should be 12
    hours = String(hours).padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds} ${ampm}`;
    
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        timeElement.innerText = timeString;
    }
}
