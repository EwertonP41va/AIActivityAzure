import os
from flask import Flask, request, jsonify
import requests
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações da API de Tradução do Azure
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION")

# Configurações da API de Fala do Azure
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")


# Função para traduzir o texto
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    to_language = data['to_language']  # Captura o idioma selecionado

    # Configura a requisição para o serviço de tradução da Azure
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION,
        'Content-Type': 'application/json'
    }
    translate_url = f"{TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={to_language}"
    body = [{'text': text}]

    response = requests.post(translate_url, headers=headers, json=body)
    translation = response.json()[0]['translations'][0]['text']

    return jsonify({"translation": translation})


# Função para converter fala em texto
@app.route('/speak', methods=['POST'])
def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Listening...")
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return jsonify({"text": result.text})
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return jsonify({"text": "Não foi possível reconhecer a fala."})
    else:
        return jsonify({"text": "Erro na captura da fala."})


# Função para sintetizar a tradução em áudio
@app.route('/play', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data['text']
    language = data['language']  # Captura o idioma selecionado

    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_language = language  # Define o idioma para síntese
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return jsonify({"status": "A síntese de fala foi completada."})
    else:
        return jsonify({"status": "Erro na síntese de fala."})


if __name__ == '__main__':
    app.run(debug=True)
