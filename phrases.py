import tkinter as tk


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
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=0, column=1, sticky='nsew')
        self.phrase_list = PhraseList()
        self.phrase_list.load()
        self.listbox.insert(tk.END, *self.phrase_list.phrases)

        self.fr_buttons = tk.Frame(self)
        self.fr_buttons.grid(row=0, column=0, sticky='ns')
        self.btn_book = tk.Button(
            self.fr_buttons, text='Открыть книгу', command=lambda: self.controller.show_frame('Book'))
        self.btn_book.grid(row=1, column=0, sticky='ew', padx=5)

    def add_phrase(self, phrase):
        self.phrase_list.phrases.append(phrase)
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *self.phrase_list.phrases)

    def save_phrases(self):
        self.phrase_list.dump()
