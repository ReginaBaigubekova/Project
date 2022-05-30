import tkinter as tk
from tkinter import *


class PhraseList:
    def __init__(self):
        self.phrases = []
        self.path = 'phrases.txt'

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.phrases = f.read().split('\n')
        except:
            pass

    def dump(self):
        with open(self.path, 'w+') as f:
            f.write('\n'.join(self.phrases))


class Phrases(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.listbox = tk.Listbox(self, width=25, height=20, bd=10, fg="black", highlightcolor="#ebccff",
                                  font=("Courier", 15), selectbackground="#c9a0dc")
        self.listbox.grid(row=0, column=2, rowspan=2, sticky='ew')
        self.phrase_list = PhraseList()
        self.phrase_list.load()
        self.listbox.insert(tk.END, *self.phrase_list.phrases)

        def show_selected():
            """
            show the translation of the selected word by pressing the button
            """
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(
                self.listbox.get(ANCHOR), dest='ru')
            show.config(text=result.text, fg="#9400d3", font=("Courier", 13))

        # Button shows translation of the selected word
        Button(self, text='Show Selected', command=show_selected, bg="#ffc766",
               font=("Courier", 13)).grid(row=2, column=2, sticky='ew')
        show = Label(self)
        show.grid(row=3, column=2, sticky='ew')

        # two functions for moving words
        def move_to_second():
            select_to_second = self.listbox.curselection()
            for i in select_to_second:
                self.lb2.insert(END, self.listbox.get(i))
            for i in reversed(select_to_second):
                self.listbox.delete(i)

        def move_to_first():
            select_to_first = self.lb2.curselection()
            for i in select_to_first:
                self.listbox.insert(END, self.lb2.get(i))
            for i in reversed(select_to_first):
                self.lb2.delete(i)

        # create second listbox for learned words
        self.lb2 = tk.Listbox(self, width=25, height=20, bd=10, fg="black", highlightcolor="#ebccff",
                              font=("Courier", 15), selectbackground="#c9a0dc")
        self.lb2.grid(row=0, column=4, rowspan=2, sticky='ew')
        Button(self, text=">>>", command=move_to_second, bg="#99ff99").grid(row=0, column=3, rowspan=1, sticky='ew')
        Button(self, text="<<<", command=move_to_first, bg="#ff6666").grid(row=0, column=3, rowspan=2, sticky='ew')

        self.fr_buttons = tk.Frame(self)
        self.fr_buttons.grid(row=0, column=0, sticky='ns')
        self.btn_book = tk.Button(
            self.fr_buttons, text='Открыть книгу', command=lambda: self.controller.show_frame('Book'),
            bg="#ffc766", font=("Courier", 13))
        self.btn_book.grid(row=1, column=0, sticky='ew', padx=5)

    def add_phrase(self, phrase):
        """
            add selection phrase to phrase_list
        """
        self.phrase_list.phrases.append(phrase)
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *self.phrase_list.phrases)

    def save_phrases(self):
        self.phrase_list.dump()
