import tkinter as tk
from tkinter import messagebox
import subprocess


def run_script():
    try:
        subprocess.run(["python", "gstno_update.py"], check=True)
        messagebox.showinfo("Success", "Process Completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {str(e)}")


root = tk.Tk()
root.title("KYC Automation")

btn = tk.Button(root, text="Start KYC Update", command=run_script, height=2, width=20)
btn.pack(pady=20)

root.mainloop()
