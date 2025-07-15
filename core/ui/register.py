# ui/register.py
import tkinter as tk
from tkinter import messagebox
import os
from core.auth import save_user
from core.voice_utils import record_voice

def register_window():
    def register():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Enter all details.")
            return

        save_user(username, password)
        messagebox.showinfo("Voice Recording", "Start speaking to register your voice.")
        record_voice(username, mode="register")
        messagebox.showinfo("Success", "User registered with voice.")

    window = tk.Tk()
    window.title("Voice Auth - Register")
    window.geometry("400x300")
    window.config(bg="#f0f0f0")

    tk.Label(window, text="Register", font=("Arial", 20)).pack(pady=10)
    tk.Label(window, text="Username").pack()
    entry_username = tk.Entry(window)
    entry_username.pack()
    tk.Label(window, text="Password").pack()
    entry_password = tk.Entry(window, show="*")
    entry_password.pack()

    tk.Button(window, text="Register", command=register).pack(pady=20)
    window.mainloop()
