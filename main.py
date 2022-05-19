import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import *

# select and open the required file


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


# to confirm the exit from the application
def on_closing():
    """
    asdjasdjhaksdjhasdasd

    :return: asdajsdhgasjdhgasd
    """
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        window.destroy()


# to change the background color (day and night)
def choose_color():
    color = colorchooser.askcolor()
    colorhex = color[1]
    txt_edit.config(bg=str(colorhex))


def night_color():
    txt_edit.config(bg="#363636")
    txt_edit.config(fg="white")


def day_color():
    txt_edit.config(bg="#ffe3d7")
    txt_edit.config(fg="black")


def font_size_plus():
    # txt_edit.config(fg="red")
    # txt_edit.config(font="10")
    # font_example = tkFont.Font(size=10)
    txt_edit.configure(font=tkFont.Font(size=+10))


def font_size_minus():
    # txt_edit.config(fg="red")
    # txt_edit.config(font="10")
    # font_example = tkFont.Font(size=10)
    txt_edit.configure(font=tkFont.Font(size=-10))


# creating the main window


window = tk.Tk()
window.title("Reader")
window.protocol("WM_DELETE_WINDOW", on_closing)

# app icon in the upper left corner
window.iconbitmap("book.ico")


# divide the window into sections and add buttons


window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)
btn_open = tk.Button(fr_buttons, text="Открыть", command=open_file, fg="black", bg="#ebccff")
btn_save = tk.Button(fr_buttons, text="Переименовать файл", command=rename_file, fg="black", bg="#ebccff")
btn_color = tk.Button(fr_buttons, text="Изменить цвет фона", command=choose_color, fg="black", bg="#ebccff")
# btn_day_color = tk.Button(fr_buttons, text="Day", command=day_color, fg="black", bg="#ebccff")
# btn_night_color = tk.Button(fr_buttons, text="Night", command=night_color, fg="black", bg="#ebccff")
btn_font_size_plus = tk.Button(fr_buttons, text="T+", command=font_size_plus, fg="black", bg="#ebccff")
btn_font_size_minus = tk.Button(fr_buttons, text="T-", command=font_size_minus, fg="black", bg="#ebccff")

img_day = PhotoImage(file="dd.png")
btn_new_day = tk.Button(fr_buttons, image=img_day, highlightthickness=0, bd=0, command=day_color)

img_night = PhotoImage(file="nn.png")
btn_new_night = tk.Button(fr_buttons, image=img_night, highlightthickness=0, bd=0, command=night_color)

btn_open.grid(row=0, column=0, columnspan=2, sticky="ew", padx=6, pady=1)
btn_save.grid(row=1, column=0, columnspan=2,  sticky="ew", padx=6, pady=1)
btn_color.grid(row=2, column=0, columnspan=2,  sticky="ew", padx=6, pady=1)
# btn_day_color.grid(row=3, column=1, padx=6, pady=1)
# btn_night_color.grid(row=4, column=1, padx=6, pady=1)
btn_font_size_plus.grid(row=3, column=0, padx=6, pady=1)
btn_font_size_minus.grid(row=4, column=0, padx=6, pady=1)

btn_new_day.grid(row=3, column=1, padx=6, pady=1)
btn_new_night.grid(row=4, column=1, padx=6, pady=1)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
