import requests
import pyaudio
import wave
import threading
import pyttsx3

# Chatbot API (DialoGPT) from huggingface
CHAT_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
# Audio Transcription API (wav2vec2) from huggingface
TRANSCRIBE_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h-lv60-self"
# Replace empty space with API key here
API_KEY = {"Authorization": "Bearer ___________________________________________"}

# Text to Speech Variables
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# TtoS engine initialization and configuration
speechEngine = pyttsx3.init()
speechEngine.setProperty('rate', 150)
speechEngine.setProperty('volume', 0.7)
voices = speechEngine.getProperty('voices')
speechEngine.setProperty('voice', voices[1].id)

# Chatbot Variables
pastResponses = []
pastInputs = []

def speakOutput(out):
	global speechEngine
	speechEngine.say(out)
	speechEngine.runAndWait()

def transcribe(filename):
	with open(filename, "rb") as f:
		data = f.read()
	response = requests.post(TRANSCRIBE_URL, headers=API_KEY, data=data)
	return response.json()

def chatQuery(pastResponses, pastInputs):
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

def startProcess(tkContainer):
	global pastResponses
	global pastInputs

	# Update the label text
	tkContainer.chatLabel.config(text="Recording")
	# Update the widget display immediately
	tkContainer.chatLabel.update_idletasks()
 
	audio = pyaudio.PyAudio()

	# open microphone stream
	stream = audio.open(format=FORMAT, channels=CHANNELS,
					rate=RATE, input=True,
					frames_per_buffer=CHUNK)
					
	frames = []

	# record for the specified number of seconds
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
		
	# Update the label text
	tkContainer.chatLabel.config(text="Finsihed Recording")
	# Update the widget display immediately
	tkContainer.chatLabel.update_idletasks()

	# stop the stream and close the audio device
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# save the recorded data as a wave file
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(audio.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	# Get the "Chatbot's response"
	output = chatQuery(pastResponses, pastInputs)
	response = output['generated_text']
	pastResponses = output['conversation']['generated_responses']
	pastInputs = output['conversation']['past_user_inputs']

	# Update the label text
	tkContainer.chatLabel.config(text=response)
	# Update the widget display immediately
	tkContainer.chatLabel.update_idletasks()

	speakOutput(response)



