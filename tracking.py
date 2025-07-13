import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Camera Viewer")
        self.window.geometry("700x550")

        self.video_label = Label(self.window)
        self.video_label.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        self.btn_start = Button(self.button_frame, text="Open Camera", command=self.start_camera)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = Button(self.button_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.cap = None
        self.running = False

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.update_frame()

    def update_frame(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.window.after(10, self.update_frame)
        else:
            self.stop_camera()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='')
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
