


document.getElementById('audioFile').addEventListener('change', function() {

    const form = document.getElementById('uploadForm');
    const formData = new FormData(form); // Get form data
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear previous results

    const loadingSpinner = document.createElement('div');
    loadingSpinner.id = 'loadingSpinner';
    loadingSpinner.className = 'loadingSpinner';
    loadingSpinner.style.display = 'flex'; 

    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    loadingSpinner.appendChild(spinner); 

    const loadingText = document.createElement('p');
    loadingText.textContent = 'Analyzing your file, please wait...';
    // loadingSpinner.appendChild(loadingText); 

    resultDiv.appendChild(loadingSpinner)
   
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
       
        resultDiv.innerHTML = ''; // Clear previous results

        const resultRow = document.createElement('div')
        resultRow.className = 'resultRow'
        
        const nameElement = document.createElement('h2');
        nameElement.textContent = data.filename;
        nameElement.className ='songName'
        
        const bpmElement = document.createElement('h2');
        bpmElement.textContent = `BPM: ${Math.round(data.tempo)}`; // Set BPM safely
        bpmElement.className = 'songBpm'

        const keyElement = document.createElement('h2');
        keyElement.textContent = `Key: ${data.key}`; // Set Key safely
        keyElement.className = 'songKey'

        resultRow.appendChild(nameElement);
        resultRow.appendChild(bpmElement);
        resultRow.appendChild(keyElement);
        resultDiv.appendChild(resultRow)
    })
    .catch(error => console.error('Error:', error));
});




const fakeData = {
    name: 'Cool song.mp3',
    tempo: 120,
    key: 'C major'
};

// Simulate delay like an actual fetch call
setTimeout(() => {
    // Update the page with fake data
    document.getElementById('result').innerHTML = `
        <div class='resultRow'>
            <h2 class='songName'>${fakeData.name}</h2>
            <h2 class='songBpm'>BPM: ${Math.round(fakeData.tempo)}</h2>
            <h2 class='songKey'>Key: ${fakeData.key}</h2>
        </div>
       
    `;
}, 500);