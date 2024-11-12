function translateText() {
    const inputText = document.getElementById('inputText').value;
    fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('translatedText').innerText = data.translation;
    });
}

function startSpeechToText() {
    fetch('/speak', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        document.getElementById('inputText').value = data.text;
        translateText();
    });
}

function playTranslation() {
    fetch('/play', { method: 'POST' });
}
