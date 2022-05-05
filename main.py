import tkinter as tk

from book import Book
from phrases import Phrases


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Book, Phrases):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('Book')

        def on_close():
            self.frames['Book'].save_bookmarks()
            self.frames['Phrases'].save_phrases()
            self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_close)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def add_phrase(self, phrase):
        self.frames['Phrases'].add_phrase(phrase)


if __name__ == '__main__':
    app = App()
    app.mainloop()
