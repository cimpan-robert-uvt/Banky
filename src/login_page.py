import hashlib
import customtkinter
import start_page
import forgot_password_page

from home_page import HomePage
from tkinter import * # type: ignore


class LoginPage(Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.error_color = "#f75002"
        self.parent = parent
        self.db = db

        # Entries list
        self.entry_list = []

        # dict
        self.entry_warning_dict = dict()

        # Center frame for entries and labels
        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = Label(self.center_frame, text="\n\nLog in", font=("Helvetica", 24))
        title.grid(row=0, column=1)

        empty_space = Label(self.center_frame, text='\n')
        empty_space.grid(row=1, column=1)

        # --------------
        #   Email
        # --------------
        email_label = Label(self.center_frame, text="Email address:", font=("Helvetica", 18))
        email_label.grid(row=2, column=1)

        self.email_entry = Entry(self.center_frame, font=("Helvetica", 18), width=40)
        self.email_entry.grid(row=3, column=1, pady=5)
        self.entry_list.append(self.email_entry)

        email_exclamation_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        email_exclamation_label.grid(row=3, column=2, padx=5)

        self.entry_warning_dict[self.email_entry] = email_exclamation_label

        # --------------
        #   Password
        # --------------
        password_label = Label(self.center_frame, text="Password:", font=("Helvetica", 18))
        password_label.grid(row=4, column=1)

        self.password_entry = Entry(self.center_frame, show="*", font=("Helvetica", 18), width=40)
        self.password_entry.grid(row=5, column=1, pady=5)
        self.entry_list.append(self.password_entry)

        password_exclamation_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        password_exclamation_label.grid(row=5, column=2, padx=5)

        self.entry_warning_dict[self.password_entry] = password_exclamation_label

        self.error_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.error_label.grid(row=6, column=1, pady=5)


        self.forgot_password = Label(self.center_frame, text="Forgot password", font=("Helvetica", 10))
        self.forgot_password.grid(row=7, column=1, pady=5)
        self.forgot_password.bind("<Button-1>",lambda e :self.forgot_password_function())


        login_button = customtkinter.CTkButton(self.center_frame, text="Log In", font=("Helvetica", 18), command=self.launch_login_page, width=180, height=40)
        login_button.grid(row=10, column=1, pady=5)

        start_button = customtkinter.CTkButton(self.center_frame, text="Start Page", font=("Helvetica", 18), command=self.launch_start_page, width=180, height=40)
        start_button.grid(row=11, column=1, pady=5)

        self.email_value = None
        self.password_value = None
        self.hashed_password = None

        # Center widgets
        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def launch_login_page(self):
        if not self.check_credentials():
            return

        home_page_frame = HomePage(self.parent, user=self.email_value, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()


    def check_credentials(self):
        self.email_value = self.email_entry.get()
        self.password_value = self.password_entry.get()
        self.hashed_password = hashlib.md5(self.password_value.encode('utf-8')).hexdigest().upper()

        self.error_label.config(text="")
        self.email_entry.config(fg="black")
        self.password_entry.config(fg="black")

        for e in self.entry_list:
            if e.get():
                self.entry_warning_dict[e].config(text="")

        ok_flag = True
        error_message = ""

        if not self.email_value:
            ok_flag = False
            self.entry_warning_dict[self.email_entry].config(text="!")

        if not self.password_value:
            ok_flag = False
            self.entry_warning_dict[self.password_entry].config(text="!")

        if self.email_value:
            if not self.db.check_if_user_exists(self.email_value):
                ok_flag = False
                self.email_entry.config(fg=self.error_color)
                self.entry_warning_dict[self.email_entry].config(text="!")
                error_message = error_message + "There is no account with this email address.\n"
            else:
                if self.password_value and not self.db.check_if_password_is_correct(self.email_value, self.hashed_password):
                    ok_flag = False
                    self.password_entry.config(fg=self.error_color)
                    self.entry_warning_dict[self.password_entry].config(text="!")
                    error_message = error_message + "Wrong password.\n"

        if error_message or not ok_flag:
            self.error_label.config(text=error_message)

        return ok_flag


    def launch_start_page(self):
        start_page_frame = start_page.StartPage(parent=self.parent, db=self.db)
        start_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        start_page_frame.tkraise()


    def forgot_password_function(self):
        forgot_password_frame = forgot_password_page.ForgotPassword(parent=self.parent, db=self.db)
        forgot_password_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        forgot_password_frame.tkraise()

