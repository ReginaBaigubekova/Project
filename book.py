import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
import json
from tkinter import *


class Library:
    def __init__(self):
        self.books = {}
        self.path = 'library.txt'

    def get_bookmark(self, name, path):
        """
            remembers the position where the reader stopped
            :returns: name and pos
        """
        if name in self.books:
            return self.books[name]['pos']
        return 0

    def edit_bookmark(self, name, position, path):
        self.books[name] = {'pos': position, 'path': path}

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.books = json.load(f)
        except:
            pass

    def dump(self):
        with open(self.path, 'w+') as f:
            json.dump(self.books, f)


# original text size
s = 10


class Book(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.library = Library()
        self.library.load()
        self.bookname = ''
        self.bookpath = ''

        self.txt_edit = tk.Text(self, state='disabled')
        self.txt_edit.grid(row=0, column=1, sticky='nsew')

        def open_file():
            """
                select and open the required file
                :returns: open file
            """
            filepath = askopenfilename(
                filetypes=[('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')]
            )
            if not filepath:
                return
            self.bookname = filepath.split('/')[-1]
            self.bookpath = filepath
            self.txt_edit.config(state='normal')
            self.txt_edit.delete('1.0', tk.END)
            with open(filepath, 'r') as input_file:
                text = input_file.read()
                self.txt_edit.insert(tk.END, text)
            self.controller.title(self.bookname)
            self.txt_edit.config(state='disabled')
            self.txt_edit.yview_moveto(
                self.library.get_bookmark(self.bookname, self.bookpath))

        def translate_selection():
            """
                translate selection phrase
            """
            from googletrans import Translator
            translator = Translator()
            filewin = tk.Toplevel(self.parent)
            translation = translator.translate(
                self.txt_edit.selection_get(), dest='ru')
            translated_text = tk.Label(filewin, text=translation.text, wraplength=300, padx=5, pady=5,
                                       fg="#EC970B", font=("Courier", 11))
            translated_text.pack()

        def save_selection():
            """
                add selection phrase to phrase_list
            """
            phrase = self.txt_edit.selection_get()
            if len(phrase) == 0:
                return
            self.controller.add_phrase(phrase)

        self.on_selection = tk.Menu(self, tearoff=0, activebackground="#c9a0dc")
        self.on_selection.add_command(
            label='Перевести', command=translate_selection)
        self.on_selection.add_command(
            label='Добавить фразу', command=save_selection)

        def do_popup(event):
            try:
                self.on_selection.tk_popup(event.x_root, event.y_root)
            finally:
                self.on_selection.grab_release()

        def choose_color():
            """
                to change the background color (day and night)

                :returns: modified text
            """

            color = colorchooser.askcolor()
            colorhex = color[1]
            self.txt_edit.config(bg=str(colorhex))

        def night_color():
            """
                changes the background color to dark and the text font to white

                :returns: modified text
            """
            self.txt_edit.config(bg="#363636")
            self.txt_edit.config(fg="white")

        def day_color():
            """
                changes the background color to light, and the text font to black

                :returns: modified text
            """
            self.txt_edit.config(bg="#DBD7D2")
            self.txt_edit.config(fg="black")

        def font_size_plus():
            """
                increase size

                :returns: modified text
            """
            global s
            s = s + 2
            self.txt_edit.config(font=("Courier", s))

        def font_size_minus():
            """
                decrease size

                :returns: modified text
            """
            global s
            s = s - 2
            self.txt_edit.config(font=("Courier", s))

        # divide the window into sections and add buttons
        self.fr_buttons = tk.Frame(self)
        self.fr_buttons.grid(row=0, column=0, sticky='ns')

        # open file button
        self.btn_open = tk.Button(
            self.fr_buttons, text='Открыть', command=open_file, fg="black", bg="#ebccff", font=("Courier", 13))
        self.btn_open.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=6, pady=1)

        # open phrase list button
        self.btn_phrase_list = tk.Button(
            self.fr_buttons, text='Открыть список фраз', command=lambda: self.controller.show_frame('Phrases'),
            fg="black", bg="#ebccff", font=("Courier", 13))
        self.btn_phrase_list.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=6, pady=1)

        # open phrase list button
        self.txt_edit.bind('<Button-3>', do_popup)

        # increase font size button
        self.btn_font_size_plus = tk.Button(self.fr_buttons, text='T+', command=font_size_plus,
                                            fg="black", bg="#ebccff", font=("Courier", 13))
        self.btn_font_size_plus.grid(row=3, column=0, padx=6, pady=1, sticky="ns")

        # reduce font size button
        self.btn_font_size_minus = tk.Button(self.fr_buttons, text="T-", command=font_size_minus,
                                             fg="black", bg="#ebccff", font=("Courier", 13))
        self.btn_font_size_minus.grid(row=4, column=0, padx=6, pady=1, sticky="ns")

        # turn on daytime mode button
        self.img_day = tk.PhotoImage(file="imgday.png")
        self.btn_new_day = tk.Button(self.fr_buttons, image=self.img_day, highlightthickness=0, bd=5, command=day_color)
        self.btn_new_day.grid(row=2, column=1, columnspan=1, padx=6, pady=1)

        # turn on nighttime mode button
        self.img_night = PhotoImage(file="imgnight.png")
        self.btn_new_night = tk.Button(self.fr_buttons, image=self.img_night,
                                       highlightthickness=0, bd=5, command=night_color)
        self.btn_new_night.grid(row=2, column=2, columnspan=1, padx=6, pady=1)

        # select any background color button
        self.img_colors = PhotoImage(file="colors.png")
        self.btn_color = tk.Button(self.fr_buttons, image=self.img_colors,
                                   highlightthickness=0, bd=5, command=choose_color)
        self.btn_color.grid(row=2, column=0, columnspan=1, padx=6, pady=1)

    def save_bookmarks(self):
        self.library.edit_bookmark(
            self.bookname, self.txt_edit.yview()[0], self.bookpath)
        self.library.dump()
