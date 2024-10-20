document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const formData = new FormData(this); // Get form data

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = ''; // Clear previous results
        
        const bpmElement = document.createElement('h2');
        bpmElement.textContent = `BPM: ${Math.round(data.tempo)}`; // Set BPM safely

        const keyElement = document.createElement('h2');
        keyElement.textContent = `Key: ${data.key}`; // Set Key safely
        
        // Append the new elements to the result div
        resultDiv.appendChild(bpmElement);
        resultDiv.appendChild(keyElement);
    })
    .catch(error => console.error('Error:', error));
});
