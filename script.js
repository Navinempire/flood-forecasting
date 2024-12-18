const apiKey = "1b4b391bd5623f17abfd8d1219da95ff"; // Replace with your OpenWeatherMap API key


document.getElementById('checkButton').addEventListener('click', () => {
    const districtName = document.getElementById('districtInput').value.trim();
    
    if (districtName) {
        checkFloodRisk(districtName);
    } else {
        alert("Please enter a district name.");
    }
});

function fetchWeatherData(cityName) {
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${apiKey}&units=metric`;
    
    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('City not found');
            }
            return response.json();
        })
        .then(data => {
            const rainfall = data.rain ? data.rain['1h'] : 0; // Rainfall in the last hour
            const temperature = data.main.temp; // Current temperature
            const weatherDescription = data.weather[0].description; // Weather description
            return { rainfall, temperature, weatherDescription };
        });
}

function checkFloodRisk(districtName) {
    // Simulated historical flood data
    const historicalData = [
        { cityName: 'Chennai', floodStartDate: '2021-11-01', floodEndDate: '2021-11-15' },
        { cityName: 'Coimbatore', floodStartDate: '2022-06-01', floodEndDate: '2022-06-10' }
        // Add more historical data as needed
    ];

    const foundHistoricalData = historicalData.find(data => data.cityName.toLowerCase() === districtName.toLowerCase());

    if (!foundHistoricalData) {
        document.getElementById('results').innerHTML = `<p>No historical flood data found for ${districtName}. Fetching today's weather instead...</p>`;
        fetchWeatherData(districtName)
            .then(weather => displayResults(districtName, weather))
            .catch(error => displayError(error.message));
    } else {
        fetchWeatherData(districtName)
            .then(weather => displayResults(districtName, weather))
            .catch(error => displayError(error.message));
    }
}

function displayResults(districtName, weather) {
    const resultsDiv = document.getElementById('results');
    
    resultsDiv.innerHTML = `
        <h2>Results for ${districtName}</h2>
        <p>Current Temperature: ${weather.temperature}°C</p>
        <p>Weather Description: ${weather.weatherDescription}</p>
        <p>Rainfall (last hour): ${weather.rainfall} mm</p>
        <p>Flood Risk: ${weather.rainfall > 10 ? 'Flood Risk Detected' : 'No Flood Risk'}</p>
    `;
}

function displayError(message) {
    const resultsDiv = document.getElementById('results');
    
    resultsDiv.innerHTML = `<p>Error: ${message}</p>`;
}
