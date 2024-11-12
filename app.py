from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import requests
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações dos serviços do Azure usando variáveis de ambiente
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION")

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

app = Flask(__name__)

def translate_text(text, to_language="es"):
    path = '/translate'
    constructed_url = TRANSLATOR_ENDPOINT + path
    params = {'api-version': '3.0', 'to': to_language}
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION,
        'Content-Type': 'application/json'
    }
    body = [{'text': text}]
    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    translation = response.json()
    return translation[0]['translations'][0]['text']

def text_to_speech(text, language="es-ES"):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_language = language
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    return result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted

def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else None

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get("text")
    target_language = data.get("to_language", "es")
    translated_text = translate_text(text, target_language)
    return jsonify({"translation": translated_text})

@app.route('/speak', methods=['POST'])
def speak():
    text = speech_to_text()
    return jsonify({"text": text}) if text else jsonify({"error": "Speech not recognized"})

@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    text = data.get("text")
    language_code = data.get("language", "es-ES")
    success = text_to_speech(text, language_code)
    return jsonify({"status": "success" if success else "failed"})

if __name__ == '__main__':
    app.run(debug=True)
