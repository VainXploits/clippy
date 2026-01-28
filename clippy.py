import time
import threading
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import messagebox
#hi
# Global flag to control typing
stop_typing_flag = False

def start_typing_thread():
    """Starts the typing process in a separate thread."""
    global stop_typing_flag
    stop_typing_flag = False
    thread = threading.Thread(target=start_typing)
    thread.daemon = True
    thread.start()

def stop_typing():
    """Stop the typing process."""
    global stop_typing_flag
    stop_typing_flag = True
    countdown_label.config(text="Typing stopped.")

def start_typing():
    """Main typing logic with 10-second delay and stop support."""
    global stop_typing_flag

    messagebox.showinfo("Clipboard Typer",
                        "Typing will begin in 10 seconds.\n"
                        "Place your cursor where you want it to type.")
    root.update()

    # Countdown before typing
    for i in range(10, 0, -1):
        if stop_typing_flag:
            countdown_label.config(text="Stopped before typing.")
            return
        countdown_label.config(text=f"Starting in {i} seconds...")
        root.update()
        time.sleep(1)

    # Get clipboard content
    try:
        text = pyperclip.paste()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get clipboard content:\n{e}")
        return

    if not text.strip():
        messagebox.showwarning("Empty Clipboard", "Clipboard is empty!")
        return

    countdown_label.config(text="Typing at GODSPEED ⚡")

    # Type as fast as possible
    pyautogui.typewrite(text, interval=0)  # interval=0 → maximum speed

    countdown_label.config(text="✅ Done typing!")

# GUI setup
root = tk.Tk()
root.title("Clipboard Typer")
root.geometry("320x200")
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

countdown_label = tk.Label(root, text="", font=("Helvetica", 11))
countdown_label.pack(pady=10)

root.mainloop()
