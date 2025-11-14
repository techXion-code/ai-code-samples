
export async function fetchWeather(city) {
    // Step 1: Get coordinates
    const { latitude, longitude } = await getGeocoordinates(city);
    // Step 2: Get weather
    const weatherRes = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`
    );
    const weatherData = await weatherRes.json();
    return weatherData.current_weather;
}
async function getGeocoordinates(city) {
    const geoRes = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${city}`);
    const geoData = await geoRes.json();
    return geoData.results[0];
}

