import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import *


def open_file():
    """
        select and open the required file

        :returns: open file
    """
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


def on_closing():
    """
        to confirm the exit from the application

        :returns: closed application
    """

    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        window.destroy()


def choose_color():
    """
        to change the background color (day and night)

        :returns: modified text
    """

    color = colorchooser.askcolor()
    colorhex = color[1]
    txt_edit.config(bg=str(colorhex))


def night_color():
    """
        changes the background color to dark and the text font to white

        :returns: modified text
    """
    txt_edit.config(bg="#363636")
    txt_edit.config(fg="white")


def day_color():
    """
        changes the background color to light, and the text font to black

        :returns: modified text
    """
    txt_edit.config(bg="#ffe3d7")
    txt_edit.config(fg="black")


# original text size
s = 10


def font_size_plus():
    """
        increase size

        :returns: modified text
    """
    global s
    s = s+3
    txt_edit.config(font=("Courier", s))


def font_size_minus():
    """
        decrease size

        :returns: modified text
    """
    global s
    s = s - 3
    txt_edit.config(font=("Courier", s))


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

btn_open = tk.Button(fr_buttons, text="Открыть файл", command=open_file, fg="black", bg="#ebccff", font=("Courier", 13))

btn_phrase_list = tk.Button(fr_buttons, text='Открыть список фраз', fg="black", bg="#ebccff", font=("Courier", 13),
                            # Команда...
                            )

btn_font_size_plus = tk.Button(fr_buttons, text="T+", command=font_size_plus,
                               fg="black", bg="#ebccff", font=("Courier", 13))

btn_font_size_minus = tk.Button(fr_buttons, text="T-", command=font_size_minus,
                                fg="black", bg="#ebccff", font=("Courier", 13))

img_day = PhotoImage(file="imgday.png")
btn_new_day = tk.Button(fr_buttons, image=img_day, highlightthickness=0, bd=5, command=day_color)

img_night = PhotoImage(file="imgnight.png")
btn_new_night = tk.Button(fr_buttons, image=img_night, highlightthickness=0, bd=5, command=night_color)

img_colors = PhotoImage(file="colors.png")
btn_color = tk.Button(fr_buttons, image=img_colors, highlightthickness=0, bd=5, command=choose_color)


#  buttons location
btn_open.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=6, pady=1)

btn_phrase_list.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=6, pady=1)

btn_color.grid(row=2, column=0, columnspan=1, padx=6, pady=1)
btn_new_day.grid(row=2, column=1, columnspan=1, padx=6, pady=1)
btn_new_night.grid(row=2, column=2, columnspan=1,  padx=6, pady=1)

btn_font_size_plus.grid(row=3, column=0, padx=6, pady=1, sticky="ns")
btn_font_size_minus.grid(row=4, column=0, padx=6, pady=1, sticky="ns")

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
