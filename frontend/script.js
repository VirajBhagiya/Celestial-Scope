let authToken = null;

// Handle Registration
document.getElementById('registrationForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const registrationMessage = document.getElementById('registrationMessage');

    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            registrationMessage.textContent = 'Registration successful! Please log in.';
        } else {
            const data = await response.json();
            registrationMessage.textContent = `Error: ${data.detail}`;
        }
    } catch (error) {
        registrationMessage.textContent = `Error: ${error.message}`;
    }
});

// Handle Login
document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const loginMessage = document.getElementById('loginMessage');

    try {
        const response = await fetch('http://127.0.0.1:8000/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            loginMessage.textContent = 'Login successful!';
            document.getElementById('coordinatesSection').style.display = 'block';
        } else {
            loginMessage.textContent = `Error: ${data.detail}`;
        }
    } catch (error) {
        loginMessage.textContent = `Error: ${error.message}`;
    }
});

// Handle Coordinate Search
document.getElementById('searchForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const celestialName = document.getElementById('celestialName').value;
    const latitude = parseFloat(document.getElementById('latitude').value);
    const longitude = parseFloat(document.getElementById('longitude').value);
    const coordinatesOutput = document.getElementById('coordinates');

    coordinatesOutput.innerHTML = `
        <h3>Coordinates</h3>
        <p><strong>RA:</strong> <span id="ra">Loading...</span></p>
        <p><strong>Dec:</strong> <span id="dec">Loading...</span></p>
        <p><strong>Azimuth:</strong> <span id="azimuth">Loading...</span></p>
        <p><strong>Altitude:</strong> <span id="altitude">Loading...</span></p>
    `;

    try {
        const response = await fetch('http://127.0.0.1:8000/get-coordinates/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
            },
            body: JSON.stringify({ name: celestialName, latitude, longitude }),
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('ra').textContent = data.coordinates.RA;
            document.getElementById('dec').textContent = data.coordinates.Dec;
            document.getElementById('azimuth').textContent = data.coordinates.Azimuth;
            document.getElementById('altitude').textContent = data.coordinates.Altitude;
        } else {
            coordinatesOutput.innerHTML = `<p>Error: ${data.detail}</p>`;
        }
    } catch (error) {
        coordinatesOutput.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
    }
});
