import tkinter as tk
from tkinter.filedialog import askopenfilename
import json


class Library:
    def __init__(self):
        self.books = {}
        self.path = 'library.txt'

    def get_bookmark(self, name, path):
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
            filepath = askopenfilename(
                filetypes=[('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')]
            )
            if not filepath:
                return
            self.bookname = filepath.split('/')[-1]
            self.bookpath = filepath
            self.txt_edit.config(state='normal')
            self.txt_edit.delete('1.0', tk.END)
            with open(filepath, 'r', encoding='utf-8') as input_file:
                text = input_file.read()
                self.txt_edit.insert(tk.END, text)
            self.controller.title(self.bookname)
            self.txt_edit.config(state='disabled')
            self.txt_edit.yview_moveto(
                self.library.get_bookmark(self.bookname, self.bookpath))

        def translate_selection():
            from googletrans import Translator
            translator = Translator()
            filewin = tk.Toplevel(self.parent)
            translation = translator.translate(
                self.txt_edit.selection_get(), dest='ru')
            translated_text = tk.Label(filewin, text=translation.text)
            translated_text.pack()

        def save_selection():
            phrase = self.txt_edit.selection_get()
            if len(phrase) == 0:
                return
            self.controller.add_phrase(phrase)

        self.on_selection = tk.Menu(self, tearoff=0)
        self.on_selection.add_command(
            label='Перевести', command=translate_selection)
        self.on_selection.add_command(
            label='Добавить фразу', command=save_selection)

        def do_popup(event):
            try:
                self.on_selection.tk_popup(event.x_root, event.y_root)
            finally:
                self.on_selection.grab_release()

        self.fr_buttons = tk.Frame(self)
        self.fr_buttons.grid(row=0, column=0, sticky='ns')
        self.btn_open = tk.Button(
            self.fr_buttons, text='Открыть', command=open_file)
        self.btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.btn_phrase_list = tk.Button(
            self.fr_buttons, text='Открыть список фраз', command=lambda: self.controller.show_frame('Phrases'))
        self.btn_phrase_list.grid(row=1, column=0, sticky='ew', padx=5)
        self.txt_edit.bind('<Button-3>', do_popup)

    def save_bookmarks(self):
        self.library.edit_bookmark(
            self.bookname, self.txt_edit.yview()[0], self.bookpath)
        self.library.dump()
