import customtkinter
import start_page
import login_page
import create_new_password_page

from tkinter import * # type: ignore


class ForgotPassword(Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.error_color = "#f75002"
        self.parent = parent
        self.db = db

        # Center frame for entries and labels
        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = Label(self.center_frame, text="\n\nRequest verification code\n\n", font=("Helvetica", 24))
        title.grid(row=0, column=1)

        empty_space = Label(self.center_frame, text='\n')
        empty_space.grid(row=1, column=1)

        # --------------
        #   Email
        # --------------
        email_label = Label(self.center_frame, text="Email address", font=("Helvetica", 18))
        email_label.grid(row=2, column=1)

        self.email_entry = Entry(self.center_frame, font=("Helvetica", 18), width=40)
        self.email_entry.grid(row=3, column=1, pady=5)

        self.email_exclamation_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.email_exclamation_label.grid(row=3, column=2, padx=5)

        empty_space = Label(self.center_frame, text='\n')
        empty_space.grid(row=4, column=1)

        self.email_warning_label = Label(self.center_frame, text="", font=("Helvetica", 15), fg=self.error_color)
        self.email_warning_label.grid(row=5, columnspan=2, padx=5)

        empty_space = Label(self.center_frame, text='\n')
        empty_space.grid(row=6, column=1)

        send_code_button = customtkinter.CTkButton(self.center_frame, text="Send Code", font=("Helvetica", 18), command=self.launch_new_password_page, width=180, height=40)
        send_code_button.grid(row=10, columnspan=2, pady=5)

        login_button = customtkinter.CTkButton(self.center_frame, text="Login Page", font=("Helvetica", 18), command=self.launch_login_page, width=180, height=40)
        login_button.grid(row=11, columnspan=2, pady=5)

        self.email_value = None

        # Center widgets
        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def launch_new_password_page(self):
        if not self.validate_user_input():
            return

        create_new_password_frame = create_new_password_page.CreateNewPassword(self.parent, db=self.db, email=self.email_value)
        create_new_password_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        create_new_password_frame.tkraise()
    

    def validate_user_input(self):
        self.email_value = self.email_entry.get()
        self.email_warning_label.config(text="")
        self.email_exclamation_label.config(text = "")
        ok_flag = True

        if not self.email_value:
            ok_flag = False
            self.email_exclamation_label.config(text= "!")
        else:
            if not self.db.check_if_user_exists(self.email_value):
                ok_flag = False
                self.email_warning_label.config(text="There is no account with this email address.")
        return ok_flag


    def launch_start_page(self):
        start_page_frame = start_page.StartPage(parent=self.parent, db=self.db)
        start_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        start_page_frame.tkraise()


    def launch_login_page(self):
        login_page_frame = login_page.LoginPage(self.parent, db=self.db)
        login_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        login_page_frame.tkraise()

