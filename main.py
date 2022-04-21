import tkinter as tk
from tkinter.filedialog import askopenfilename

from pyparsing import col


class Book(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        txt_edit = tk.Text(self)
        txt_edit.grid(row=0, column=1, sticky='nsew')

        def open_file():
            filepath = askopenfilename(
                filetypes=[('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')]
            )
            if not filepath:
                return
            txt_edit.delete('1.0', tk.END)
            with open(filepath, 'r', encoding='utf-8') as input_file:
                text = input_file.read()
                txt_edit.insert(tk.END, text)
            controller.title(filepath)

        def translate_selection():
            from googletrans import Translator
            translator = Translator()
            filewin = tk.Toplevel(self.parent)
            translation = translator.translate(
                txt_edit.selection_get(), dest='ru')
            translated_text = tk.Label(filewin, text=translation.text)
            translated_text.pack()

        def save_selection():
            if len(txt_edit.selection_get()) == 0:
                return
            with open('phrases.txt', 'a') as phrases_file:
                phrases_file.write(txt_edit.selection_get() + '\n')

        on_selection = tk.Menu(self, tearoff=0)
        on_selection.add_command(
            label='Translate', command=translate_selection)
        on_selection.add_command(label='Add word', command=save_selection)

        def do_popup(event):
            try:
                on_selection.tk_popup(event.x_root, event.y_root)
            finally:
                on_selection.grab_release()

        fr_buttons = tk.Frame(self)
        fr_buttons.grid(row=0, column=0, sticky='ns')
        btn_open = tk.Button(fr_buttons, text='Открыть', command=open_file)
        btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        btn_phrase_list = tk.Button(
            fr_buttons, text='Открыть список фраз', command=lambda: controller.show_frame('PhraseList'))
        btn_phrase_list.grid(row=1, column=0, sticky='ew', padx=5)
        txt_edit.bind('<Button-3>', do_popup)


class PhraseList(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        label = tk.Label(self, text='asd')
        label.grid(row=0, column=1, sticky='nsew')

        fr_buttons = tk.Frame(self)
        fr_buttons.grid(row=0, column=0, sticky='ns')
        btn_book = tk.Button(
            fr_buttons, text='Открыть книгу', command=lambda: controller.show_frame('Book'))
        btn_book.grid(row=1, column=0, sticky='ew', padx=5)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Book, PhraseList):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Book")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    app = App()
    app.mainloop()
