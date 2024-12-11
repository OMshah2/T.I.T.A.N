// Function to handle user input
function processInput() {
    var userInput = document.getElementById('input').value;

    if (userInput.trim() === "") {
        alert("Please type a query!");
        return;
    }

    // Display user input in output area (this simulates sending the input)
    document.getElementById('output').value = "You: " + userInput;

    // Call the backend API with the user input
    fetch('/process_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display the assistant's response
        document.getElementById('output').value += "\n\nTitan: " + data.response;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to handle voice input
function startRecording() {
    // Here you would implement the audio recording feature
    alert("Voice recording functionality is not implemented in this demo yet.");
}
