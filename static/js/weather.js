(function() {
    const iconMap = {
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
        0: { description: 'Clear Sky', icon: 'clear' },
        1: { description: 'Mostly Clear', icon: 'clear' },
        2: { description: 'Partly Cloudy', icon: 'partly-cloudy' },
        3: { description: 'Overcast', icon: 'overcast' },
        45: { description: 'Fog', icon: 'fog' },
        48: { description: 'Depositing Rime Fog', icon: 'fog' },
        51: { description: 'Light Drizzle', icon: 'drizzle' },
        53: { description: 'Moderate Drizzle', icon: 'drizzle' },
        55: { description: 'Heavy Drizzle', icon: 'drizzle' },
        56: { description: 'Light Freezing Drizzle', icon: 'drizzle' },
        57: { description: 'Heavy Freezing Drizzle', icon: 'drizzle' },
        61: { description: 'Light Rain', icon: 'rain' },
        63: { description: 'Moderate Rain', icon: 'rain' },
        65: { description: 'Heavy Rain', icon: 'rain' },
        66: { description: 'Light Freezing Rain', icon: 'rain' },
        67: { description: 'Heavy Freezing Rain', icon: 'rain' },
        71: { description: 'Light Snow', icon: 'snow' },
        73: { description: 'Moderate Snow', icon: 'snow' },
        75: { description: 'Heavy Snow', icon: 'snow' },
        77: { description: 'Snow Grains', icon: 'sleet' },
        80: { description: 'Light Rain Showers', icon: 'rain' },
        81: { description: 'Moderate Rain Showers', icon: 'rain' },
        82: { description: 'Heavy Rain Showers', icon: 'rain' },
        85: { description: 'Light Snow Showers', icon: 'snow' },
        86: { description: 'Heavy Snow Showers', icon: 'snow' },
        95: { description: 'Thunderstorm', icon: 'thunderstorms-rain' },
        96: { description: 'Thunderstorm with Light Hail', icon: 'thunderstorms-snow' },
        99: { description: 'Thunderstorm with Heavy Hail', icon: 'thunderstorms-snow' }
    };

    function getWeatherIconURL(code) {
        if (code === null || Number.isNaN(code)) {
            return iconMap['partly-cloudy'];
        }

        const weather = weatherCodes[code];
        if (!weather) {
            return iconMap['partly-cloudy'];
        }

        return iconMap[weather.icon] || iconMap['partly-cloudy'];
    }

    function resolveDescription(code) {
        if (code === null || Number.isNaN(code)) {
            return 'Forecast unavailable';
        }

        const weather = weatherCodes[code];
        return weather ? weather.description : 'Forecast unavailable';
    }

    function setContent() {
        const forecastCards = document.querySelectorAll('[data-forecast-code]');
        if (!forecastCards.length) {
            return;
        }

        forecastCards.forEach(card => {
            const rawCode = card.getAttribute('data-forecast-code');
            const parsedCode = rawCode === '' ? null : parseInt(rawCode, 10);
            const iconElement = card.querySelector('.forecast-icon');
            const descriptionElement = card.querySelector('[data-forecast-desc]');
            const description = resolveDescription(parsedCode);

            if (iconElement) {
                iconElement.src = getWeatherIconURL(parsedCode);
                iconElement.alt = description;
            }

            if (descriptionElement) {
                descriptionElement.textContent = description;
            }
        });
    }

    window.setContent = setContent;
})();