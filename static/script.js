
document.getElementById('audioFile').addEventListener('change', function() {


    const loadingSpinner = document.createElement('div');
    loadingSpinner.id = 'loadingSpinner';
    loadingSpinner.className = 'loadingSpinner';
    loadingSpinner.style.display = 'flex'; 

    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    loadingSpinner.appendChild(spinner); 

    
    
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear previous results


    const audioFile = document.getElementById('audioFile');
    const files = audioFile.files;

    async function uploadFilesSequentially(files) {
        
        for (const file of files) {
            resultDiv.appendChild(loadingSpinner)
            await uploadFile(file); // Wait for each file to finish processing before moving to the next
            
        }
        loadingSpinner.remove()
    }
    
    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('audioFile', file);
    
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            //You need the await keyword before 
            //response.json() because response.json() returns a Promise.
            const data = await response.json();
    
            // Process the response data for the current file
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    function displayResults(data) {
        const resultRow = document.createElement('div');
        resultRow.className = 'resultRow';
    
        const nameElement = document.createElement('h2');
        nameElement.textContent = data.filename;
        nameElement.className = 'songName';
    
        const bpmElement = document.createElement('h2');
        bpmElement.textContent = `BPM: ${Math.round(data.tempo)}`;
        bpmElement.className = 'songBpm';
    
        const keyElement = document.createElement('h2');
        keyElement.textContent = `Key: ${data.key}`;
        keyElement.className = 'songKey';
    
        resultRow.appendChild(nameElement);
        resultRow.appendChild(bpmElement);
        resultRow.appendChild(keyElement);
        resultDiv.appendChild(resultRow);
    }
    
    // Usage: pass in the files array
    uploadFilesSequentially(files);
});




const fakeDataArray = [
    { name: 'Cool song 1.mp3', tempo: 120, key: 'C major' },
    { name: 'Cool song 2.mp3', tempo: 130, key: 'G major' },
    { name: 'Cool song 3.mp3', tempo: 115, key: 'D minor' },
    { name: 'Cool song 4.mp3', tempo: 125, key: 'A major' },
    { name: 'Cool song 5.mp3', tempo: 140, key: 'E minor' },
    { name: 'Cool song 6.mp3', tempo: 110, key: 'B major' },
    { name: 'Cool song 7.mp3', tempo: 135, key: 'F# minor' },
    { name: 'Cool song 8.mp3', tempo: 150, key: 'C# major' },
    { name: 'Cool song 9.mp3', tempo: 145, key: 'E major' },
    { name: 'Cool song 10.mp3', tempo: 155, key: 'G minor' },
];

// Function to simulate fetching and updating the result
function simulateFetchingData() {
    fakeDataArray.forEach((data, index) => {
        setTimeout(() => {
            document.getElementById('result').innerHTML += `
                <div class='resultRow'>
                    <h2 class='songName'>${data.name}</h2>
                    <h2 class='songBpm'>BPM: ${Math.round(data.tempo)}</h2>
                    <h2 class='songKey'>Key: ${data.key}</h2>
                </div>
            `;
        }); // Delay each row by 500ms
    });
}

// Call the function to start simulating
simulateFetchingData();