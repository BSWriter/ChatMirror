import tkinter as tk
import random
import chatScript as chatbot
import time
import threading

class MainMirror(tk.Tk):
        def __init__(self):
                tk.Tk.__init__(self)
                # Set Container attributes
                self.attributes('-fullscreen', True)
                self.configure(bg='black')

                # Initialize class variables
                self.numthreads = 0
                self.max_numthreads = 2
                self.alpha = 0
                self.alphaDelta = 5
                self.chatThread = threading.Thread(target=chatbot.startProcess, args=(self,))
                self.activeThreads = {"chat":None}
                self.updateTime = 50 # Milliseconds for update loop 
                self.blinkWait = 1000 # Milliseconds for timeLabel to startup blinking animation
                
                # Initialize Chatbot Label, place in center
                self.chatLabel = tk.Label(self, text=self.startup(), font=("Helvetica", 36), fg="white", bg="black", wraplength=1000)
                self.chatLabel.pack(expand=True)

                # Initialize Time Label, place in the upper left corner
                self.timeLabel = tk.Label(self, font=("Helvetica", 26), fg=f"#{self.alpha:02x}{self.alpha:02x}{self.alpha:02x}", bg="black")
                self.timeLabel.place(relx = 0.0, rely = 0.0, anchor ='nw')

                # Keybindings
                self.bind('<Alt-q>', self.quit_app)
                self.bind("<space>", self.on_space_press)

                # Start update
                self.update()
                # NUM_THREADS += 1

        def startup(self):
                openers = ["Good Morning.", "Howdy!", "How's the day going?", "Hmmm?"]
                return random.choice(openers)
        
        def quit_app(self, event=None):
                for k, v in self.activeThreads.items():
                        if v is not None:
                                v.join()
                self.destroy()
        
        # If SPACE is pressed, start chatbot process
        def on_space_press(self, event):
                if(not self.chatThread.is_alive() and self.numthreads < self.max_numthreads 
                   and self.activeThreads["chat"] is None):
                        self.numthreads += 1
                        self.chatThread = threading.Thread(target=chatbot.startProcess, args=(self,))
                        self.activeThreads["chat"] = self.chatThread
                        self.chatThread.start()

        def update(self):
                # Update Time label display
                current_time = time.strftime("%H:%M:%S")
                self.timeLabel.config(text=current_time)
                self.timeLabel.update_idletasks()

                # Handle Time label blinking
                if self.blinkWait <= 0:
                        alpha = self.alpha
                        alphaDelta = self.alphaDelta
                        
                        alpha += alphaDelta
                        self.timeLabel.config(fg=f"#{alpha:02x}{alpha:02x}{alpha:02x}")
                        self.timeLabel.update_idletasks()
                        
                        if alpha >= 105:
                                alpha = 105
                                alphaDelta = -5
                                self.blinkWait = 1000
                        elif alpha <= 25:
                                alpha = 25
                                alphaDelta = 5

                        self.alpha = alpha
                        self.alphaDelta = alphaDelta
                else:
                        self.blinkWait -= self.updateTime

                for k, v in self.activeThreads.items():
                        if v is not None:
                                if not v.is_alive():
                                        self.numthreads -= 1
                                        v.join()
                                        self.activeThreads[k] = None

                self.after(self.updateTime, self.update)
