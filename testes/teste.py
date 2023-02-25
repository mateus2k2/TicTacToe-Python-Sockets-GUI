import threading
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Load GIF image
        self.gif = Image.open('loading.gif')
        self.gif_frames = []
        self.load_gif_frames()

        # Create a label to display the GIF image
        self.label = tk.Label(self.frame)
        self.label.pack()

        # Start a thread to run a time-consuming task
        self.thread = threading.Thread(target=self.run_task)
        self.thread.start()

        # Start playing the GIF image
        self.play_gif()

    def load_gif_frames(self):
        try:
            while True:
                self.gif_frames.append(ImageTk.PhotoImage(self.gif.copy()))
                self.gif.seek(len(self.gif_frames))
        except EOFError:
            pass

    def play_gif(self, frame_index=0):
        # Display the current frame of the GIF image
        self.label.config(image=self.gif_frames[frame_index])

        # Go to the next frame of the GIF image
        next_frame_index = (frame_index + 1) % len(self.gif_frames)

        # Check if the thread is still running
        if self.thread.is_alive():
            # Schedule the next frame of the GIF image to be displayed
            self.master.after(3, self.play_gif, next_frame_index)

    def run_task(self):
        # Replace this with your time-consuming task
        import time
        time.sleep(50)

        # Update the GUI when the task is done
        self.master.after(0, self.task_done)

    def task_done(self):
        # Stop playing the GIF image and remove it from the GUI
        self.label.config(image=None)
        self.label.pack_forget()

        # Display a message to indicate that the task is done
        self.task_label = tk.Label(self.frame, text='Task done!')
        self.task_label.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()