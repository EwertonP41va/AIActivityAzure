function getSelectedLanguage() {
    return document.getElementById('languageSelect').value;
}

function translateText() {
    const inputText = document.getElementById('inputText').value;
    const targetLanguage = getSelectedLanguage();
    fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText, to_language: targetLanguage })
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
    const text = document.getElementById('translatedText').innerText;
    const targetLanguage = getSelectedLanguage();
    fetch('/play', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, language: targetLanguage })
    });
}
