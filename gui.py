

import tkinter as tk
import subprocess

def start_capture():
    streamer = entry_streamer.get()
    detection_text = entry_detection_text.get()
    subprocess.Popen(["python", "detectChats.py", streamer, detection_text])

def end_clip():
    with open('end_clip.txt', 'w') as file:
        file.write('')  # Write an empty string to the file

root = tk.Tk()
root.geometry("300x200")  # Set the window size to 300x200
root.title("Money Machine")  # Set the window title

tk.Label(root, text="Streamer:").pack(fill=tk.X, padx=5, pady=5)
entry_streamer = tk.Entry(root)
entry_streamer.pack(fill=tk.X, padx=5, pady=5)

tk.Label(root, text="Detection Text:").pack(fill=tk.X, padx=5, pady=5)
entry_detection_text = tk.Entry(root)
entry_detection_text.pack(fill=tk.X, padx=5, pady=5)

start_button = tk.Button(root, text="Start Capture", command=start_capture)
start_button.pack(fill=tk.X, padx=5, pady=5)

end_button = tk.Button(root, text="End Clip", command=end_clip)
end_button.pack(fill=tk.X, padx=5, pady=5)

root.mainloop()
