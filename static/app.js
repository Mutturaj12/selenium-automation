// app.js
document.getElementById('seleniumForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const url = document.getElementById('urlInput').value;
    const flow = document.getElementById('flowInput').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url, user_flow: flow })
    });

    const result = await response.json();
    const output = document.getElementById('output');

    if (response.ok) {
        output.textContent = result.code;
    } else {
        output.textContent = `Error: ${result.error}`;
    }
});