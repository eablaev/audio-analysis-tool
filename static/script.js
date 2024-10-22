


document.getElementById('audioFile').addEventListener('change', function() {

    const form = document.getElementById('uploadForm');
    const formData = new FormData(form); // Get form data

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = ''; // Clear previous results

        const nameElement = document.createElement('h2');
        nameElement.textContent = data.filename;
        nameElement.className ='songName'
        
        const bpmElement = document.createElement('h2');
        bpmElement.textContent = `BPM: ${Math.round(data.tempo)}`; // Set BPM safely
        bpmElement.className = 'songBpm'

        const keyElement = document.createElement('h2');
        keyElement.textContent = `Key: ${data.key}`; // Set Key safely
        keyElement.className = 'songKey'

        // Append the new elements to the result div
        resultDiv.appendChild(nameElement);
        resultDiv.appendChild(bpmElement);
        resultDiv.appendChild(keyElement);
    })
    .catch(error => console.error('Error:', error));
});




//testing


const fakeData = {
    name: 'Cool song.mp3',
    tempo: 120,
    key: 'C major'
};

// Simulate delay like an actual fetch call
setTimeout(() => {
    // Update the page with fake data
    document.getElementById('result').innerHTML = `
        <h2 class='songName'>${fakeData.name}</h2>
        <h2 class='songBpm'>BPM: ${Math.round(fakeData.tempo)}</h2>
        <h2 class='songKey'>Key: ${fakeData.key}</h2>
    `;
}, 500); // Simulate a 500ms delay