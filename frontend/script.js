document.getElementById('searchForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const celestialName = document.getElementById('celestialName').value;
    const coordinatesOutput = document.getElementById('coordinates');
    
    // Show loading message without overwriting the entire content
    coordinatesOutput.innerHTML = `
        <h2>Coordinates</h2>
        <p><strong>RA:</strong> <span id="ra">Loading...</span></p>
        <p><strong>Dec:</strong> <span id="dec">Loading...</span></p>
        <p><strong>Azimuth:</strong> <span id="azimuth">Loading...</span></p>
        <p><strong>Altitude:</strong> <span id="altitude">Loading...</span></p>
    `;
    
    try {
        const response = await fetch('http://127.0.0.1:8000/get-coordinates/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: celestialName }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Update the coordinates with the actual data
            document.getElementById('ra').textContent = data.coordinates.RA;
            document.getElementById('dec').textContent = data.coordinates.Dec;
            document.getElementById('azimuth').textContent = data.coordinates.Azimuth;
            document.getElementById('altitude').textContent = data.coordinates.Altitude;
        } else {
            coordinatesOutput.innerHTML = `<p>Error: ${data.message}</p>`;
        }
    } catch (error) {
        coordinatesOutput.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
    }
});
