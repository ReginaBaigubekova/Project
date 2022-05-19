import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


def open_file():
    filepath = askopenfilename(
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r", encoding='utf-8') as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Reader - {filepath}")


def rename_file():
    import os
    filepath = askopenfilename(
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    file = open(filepath)
    os.rename(file.name, "C:\\Users\\Regina\\Documents\\УНИВЕР\\test.txt")


def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        window.destroy()


def choose_color():
    color = colorchooser.askcolor()
    colorhex = color[1]
    print(colorhex)
    txt_edit.config(bg=str(colorhex))


def night_color():
    txt_edit.config(bg="#363636")
    txt_edit.config(fg="white")


def day_color():
    txt_edit.config(bg="#ffe3d7")
    txt_edit.config(fg="black")


window = tk.Tk()
window.title("Reader")
window.protocol("WM_DELETE_WINDOW", on_closing)

window.iconbitmap("book-g6a15db4e8_640.ico")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)
btn_open = tk.Button(fr_buttons, text="Открыть", command=open_file, fg="black", bg="#ebccff")
btn_save = tk.Button(fr_buttons, text="Переименовать файл", command=rename_file, fg="black", bg="#ebccff")
btn_color = tk.Button(fr_buttons, text="Изменить цвет фона", command=choose_color, fg="black", bg="#ebccff")
btn_day_color = tk.Button(fr_buttons, text="Day", command=day_color, fg="black", bg="#ebccff")
btn_night_color = tk.Button(fr_buttons, text="Night", command=night_color, fg="black", bg="#ebccff")

btn_open.grid(row=0, column=0, columnspan=2, sticky="ew", padx=6, pady=1)
btn_save.grid(row=1, column=0, columnspan=2,  sticky="ew", padx=6, pady=1)
btn_color.grid(row=2, column=0, columnspan=2,  sticky="ew", padx=6, pady=1)
btn_day_color.grid(row=3, column=0, padx=6, pady=1)
btn_night_color.grid(row=3, column=1, padx=6, pady=1)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
