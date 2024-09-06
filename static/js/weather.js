// Map the icon names to their respective URLs
const iconMap = {
    'clear': 'https://basmilius.github.io/weather-icons/production/fill/all/clear-day.svg', // Clear sky
    'partly-cloudy': 'https://basmilius.github.io/weather-icons/production/fill/all/partly-cloudy-day.svg', // Partly cloudy
    'cloudy': 'https://basmilius.github.io/weather-icons/production/fill/all/cloudy.svg', // Cloudy
    'overcast': 'https://basmilius.github.io/weather-icons/production/fill/all/overcast.svg', // Overcast
    'fog': 'https://basmilius.github.io/weather-icons/production/fill/all/fog.svg', // Fog
    'drizzle': 'https://basmilius.github.io/weather-icons/production/fill/all/drizzle.svg', // Drizzle
    'rain': 'https://basmilius.github.io/weather-icons/production/fill/all/rain.svg', // Rain
    'snow': 'https://basmilius.github.io/weather-icons/production/fill/all/snow.svg', // Snow
    'sleet': 'https://basmilius.github.io/weather-icons/production/fill/all/sleet.svg', // Sleet
    'thunderstorms-rain': 'https://basmilius.github.io/weather-icons/production/fill/all/thunderstorms-rain.svg', // Thunderstorm with rain
    'thunderstorms-snow': 'https://basmilius.github.io/weather-icons/production/fill/all/thunderstorms-snow.svg', // Thunderstorm with snow
    'night-clear': 'https://basmilius.github.io/weather-icons/production/fill/all/clear-night.svg', // Clear night
};

// Define the weather codes with descriptions and icons
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

// Function to map weather codes to icon URLs using both structures
function getWeatherIconURL(weatherCode) {
    console.log(weatherCode);
    const weather = weatherCodes[weatherCode];
    if (!weather) {
        return iconMap['partly-cloudy']; // Default icon
    }
    const iconName = weather.icon;
    return iconMap[iconName] || iconMap['partly-cloudy']; // Fallback to default if icon not found
}

// Update weather icons dynamically based on the current weather and forecast
window.onload = function() {
    const weatherCode = document.getElementById('weather-desc').innerText;
    const weatherIcon = getWeatherIconURL(weatherCode);
    document.getElementById('weather-icon').src = weatherIcon;

    // Loop through forecast icons and set them
    for (let i = 0; i < 7; i++) {
        const forecastCode = document.getElementById(`forecast-icon-${i}`).dataset.code; // Replace this with your forecast code
        const forecastIcon = getWeatherIconURL(forecastCode);
        document.getElementById(`forecast-icon-${i}`).src = forecastIcon;
    }
};