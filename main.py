import tkinter as tk
from tkinter import messagebox

from book import Book
from phrases import Phrases
from tkinter import *


# creating the main window
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.title("Reader")

        # app icon in the upper left corner
        self.iconbitmap("book.ico")

        self.container.pack(side='top', fill='both', expand=True)
        self.container.rowconfigure(0, minsize=800, weight=1)
        self.container.columnconfigure(1, minsize=800, weight=1)

        self.frames = {}
        for F in (Book, Phrases):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='ns')

        self.show_frame('Book')

        def on_closing():
            """
                to confirm the exit from the application
                :returns: closed application
            """

            if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
                self.frames['Book'].save_bookmarks()
                self.frames['Phrases'].save_phrases()
                self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_closing)

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def add_phrase(self, phrase):
        self.frames['Phrases'].add_phrase(phrase)


if __name__ == '__main__':
    app = App()
    app.mainloop()
