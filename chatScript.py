import requests

# Chatbot API (DialoGPT) from huggingface
CHAT_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
# Audio Transcription API (wav2vec2) from huggingface
TRANSCRIBE_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h-lv60-self"
# Replace empty space with API key here
API_KEY = {"Authorization": "Bearer ____________________________________"}

def transcribe(filename):
	with open(filename, "rb") as f:
		data = f.read()
	response = requests.post(TRANSCRIBE_URL, headers=API_KEY, data=data)
	return response.json()

def ChatQuery(pastResponses, pastInputs):
	text = transcribe("output.wav")['text']
	text = text.lower()
	
	payload = {"inputs": {
		"past_user_inputs": pastResponses,
		"generated_responses": pastInputs,
		"text": text
	},}
	
	print(payload)
	
	response = requests.post(CHAT_URL, headers=API_KEY, json=payload)
	result = response.json()
	
	print(result)
	return result

