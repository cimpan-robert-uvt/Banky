import start_page

from tkinter import * # type: ignore
from db_utils import DB


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Banky")
        self.center_window(700, 780)

        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)

        self.db = DB()

        self.container.grid_columnconfigure(0, weight=1)
        self.update_idletasks()

        start_page_frame = start_page.StartPage(parent=self.container, db=self.db)
        start_page_frame.grid(row=0, column=0, sticky="nsew")
        start_page_frame.tkraise()


    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = ((screen_height // 2) - 40)  - (height // 2)

        self.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
