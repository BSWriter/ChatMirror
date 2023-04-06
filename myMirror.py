import tkinter as tk
import random
import pyaudio
import wave
import threading
import pyttsx3
import chatScript as chatbot

# Text to Speech Variables
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Chatbot Variables
pastResponses = []
pastInputs = []

class MainMirror(tk.Tk):
        def __init__(self):
                tk.Tk.__init__(self)
                self.attributes('-fullscreen', True)
                self.configure(bg='black')
                
                # Initialize Mirror Text
                self.label = tk.Label(self, text=self.startup(), font=("Helvetica", 36), fg="white", bg="black", wraplength=1000)
                self.label.pack(expand=True)
                #anim.pulseAnim(self.label)

                # Keybindings
                self.bind('<Alt-q>', self.quit_app)
                self.bind("<space>", self.on_space_press)
                
                # TtoS engine initialization and configuration
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.7)
                voices = self.engine.getProperty('voices')
                self.engine.setProperty('voice', voices[1].id)

        def startup(self):
                openers = ["Good Morning.", "Howdy!", "How's the day going?", "Hmmm?"]
                return random.choice(openers)
        
        def quit_app(self, event=None):
                self.destroy()
        
        def speakOutput(self, out):
                self.engine.say(out)
                self.engine.runAndWait()
    
        def on_space_press(self, event):
                global pastResponses
                global pastInputs
                    
                # Update the label text
                self.label.config(text="Recording")
                # Update the widget display immediately
                self.label.update_idletasks()
                
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
                self.label.config(text="Finsihed Recording")
                # Update the widget display immediately
                self.label.update_idletasks()

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
                output = chatbot.ChatQuery(pastResponses, pastInputs)
                response = output['generated_text']
                pastResponses = output['conversation']['generated_responses']
                pastInputs = output['conversation']['past_user_inputs']
                
                # Update the label text
                self.label.config(text=response)
                # Update the widget display immediately
                self.label.update_idletasks()
                
                self.speakOutput(response)


