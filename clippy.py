import time
import threading
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import messagebox, ttk

stop_typing_flag = False
typing_speed = 0.03  # default speed

def start_typing_thread():
    global stop_typing_flag
    stop_typing_flag = False
    thread = threading.Thread(target=start_typing)
    thread.daemon = True
    thread.start()

def stop_typing():
    global stop_typing_flag
    stop_typing_flag = True
    countdown_label.config(text="Typing stopped.")

def start_typing():
    global stop_typing_flag, typing_speed

    messagebox.showinfo("Clipboard Typer",
                        "Typing will begin in 10 seconds.\n"
                        "Place your cursor where you want it to type.")
    root.update()

    # Countdown
    for i in range(10, 0, -1):
        if stop_typing_flag:
            countdown_label.config(text="Stopped before typing.")
            return
        countdown_label.config(text=f"Starting in {i} seconds...")
        root.update()
        time.sleep(1)

    # Get clipboard
    try:
        text = pyperclip.paste()
    except Exception as e:
        messagebox.showerror("Error", f"Clipboard read failed:\n{e}")
        return

    if not text.strip():
        messagebox.showwarning("Empty Clipboard", "Clipboard is empty!")
        return

    countdown_label.config(text="Typing...")

    # Type safely with proper spacing
    for char in text:
        if stop_typing_flag:
            countdown_label.config(text="Typing stopped.")
            return

        if char == '\n':
            pyautogui.press('enter')
            time.sleep(typing_speed * 5)  # add a bit more delay for newlines
        elif char == '\t':
            pyautogui.press('tab')
            time.sleep(typing_speed)
        else:
            pyautogui.typewrite(char)
            time.sleep(typing_speed)

    countdown_label.config(text="✅ Done typing!")

def update_speed(event=None):
    global typing_speed
    val = speed_slider.get()
    typing_speed = max(0.005, float(val) / 1000.0)
    speed_label.config(text=f"Typing Speed: {val} ms/char")

# GUI setup
root = tk.Tk()
root.title("Clipboard Typer")
root.geometry("360x260")
root.resizable(False, False)

title_label = tk.Label(root, text="Clipboard Typer", font=("Helvetica", 14, "bold"))
title_label.pack(pady=10)

info_label = tk.Label(root, text="Copies the latest clipboard and types it\n"
                                 "wherever the cursor is active.", justify="center")
info_label.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start", command=start_typing_thread,
                         width=12, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_typing,
                        width=12, bg="#F44336", fg="white", font=("Helvetica", 10, "bold"))
stop_button.grid(row=0, column=1, padx=5)

# Speed control
speed_label = tk.Label(root, text="Typing Speed: 30 ms/char")
speed_label.pack(pady=5)
speed_slider = ttk.Scale(root, from_=5, to=200, orient='horizontal', command=update_speed)
speed_slider.set(30)
speed_slider.pack(pady=5, fill="x", padx=30)

countdown_label = tk.Label(root, text="", font=("Helvetica", 11))
countdown_label.pack(pady=10)

root.mainloop()

