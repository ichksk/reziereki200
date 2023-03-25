import tkinter as tk
from tkinter import filedialog

def print_text():
    """テキストフォームの内容をprintする関数"""
    print(entry.get())

def open_file_dialog():
    """ファイルダイアログを開く関数"""
    filepath = filedialog.askopenfilename()
    print("Selected file:", filepath)

root = tk.Tk()

# テキストフォームを作成
entry = tk.Entry(root, width=30)
entry.grid(row=0, column=0, padx=10, pady=10)

# ボタンを作成
button_print = tk.Button(root, text="Print", command=print_text)
button_print.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# ファイルダイアログを作成
button_file = tk.Button(root, text="Open File", command=open_file_dialog)
button_file.grid(row=0, column=1, padx=10, pady=10, sticky="e")

root.mainloop()