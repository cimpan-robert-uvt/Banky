import customtkinter
import tkinter as tk
import login_page
import create_account_page

from PIL import Image, ImageTk


class StartPage(tk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db

        self.center_frame = tk.Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(self.center_frame, text="\n\nWelcome to Banky!\n\n\n", font=("Helvetica", 24))
        label.grid(row=0, column=0)


        image_path = "mobile-payment.png"
        image = Image.open(image_path)
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.center_frame, image=photo)
        image_label.image = photo # type: ignore
        image_label.grid(row=1, column=0)

        empty_space2 = tk.Label(self.center_frame, text='\n\n\n\n')
        empty_space2.grid(row=2, column=0)

        login_button = customtkinter.CTkButton(self.center_frame, text="Log In", font=("Helvetica", 18), command= self.launch_login_page, width=180, height=40)
        login_button.grid(row=3, column=0, pady = 5, padx = 5)

        create_account_button = customtkinter.CTkButton(self.center_frame, text="Create Account", font=("Helvetica", 18), command=self.launch_create_account_page, width=180, height=40)
        create_account_button.grid(row=4, column=0, pady = 5, padx = 5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pack_widgets()

    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def launch_login_page(self):

        login_page_frame = login_page.LoginPage(parent=self.parent, db=self.db)
        login_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        login_page_frame.tkraise()

    def launch_create_account_page(self):

        create_account_page_frame = create_account_page.CreateAccountPage(parent=self.parent, db=self.db)
        create_account_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        create_account_page_frame.tkraise()
