import hashlib
import customtkinter
import random
import login_page

from tkinter import * # type: ignore
from utils import send_mail


class CreateNewPassword(Frame):
    def __init__(self, parent, db, email):
        super().__init__(parent)
        self.error_color = "#f75002"
        self.parent = parent
        self.db = db
        self.email = email
        self.uid = db.get_uid(self.email)

        self.verification_code = random.randrange(1000,9999)
        send_mail(self.email,"Account verification code", f"Hello, \nYour verification code is: {self.verification_code}. Use it to create a new password.")

        # Center frame for entries and labels
        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = Label(self.center_frame, text="\n\nCreate new password\n\n", font=("Helvetica", 24))
        title.grid(row=0, columnspan=2)

        empty_space = Label(self.center_frame, text='\n')
        empty_space.grid(row=1)
 
        # --------------
        #   Password
        # --------------
        password_1_label = Label(self.center_frame, text="New Password: ", font=("Helvetica", 18))
        password_1_label.grid(row=2, column=0)

        self.password_1_entry = Entry(self.center_frame, show="*", font=("Helvetica", 18), width=30)
        self.password_1_entry.grid(row=2, column=1, pady=10)

        self.password_exclamation_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.password_exclamation_label.grid(row=2, column=2)

        # -------------------
        #   Repeat Password
        # -------------------
        password_2_label = Label(self.center_frame, text="Repeat New Password:", font=("Helvetica", 18))
        password_2_label.grid(row=3, column=0)

        self.password_2_entry = Entry(self.center_frame, show="*", font=("Helvetica", 18), width=30)
        self.password_2_entry.grid(row=3, column=1, pady=10)

        self.repeat_password_exclamation_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.repeat_password_exclamation_label.grid(row=3, column=2)

        # -------------------
        #   Verification Code
        # -------------------
        verification_code_label = Label(self.center_frame, text="Verification Code:", font=("Helvetica", 18))
        verification_code_label.grid(row=4, column=0)

        self.verification_code_entry = Entry(self.center_frame, font=("Helvetica", 18), width=30)
        self.verification_code_entry.grid(row=4, column=1, pady=10)

        self.verification_code_exclamation_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.verification_code_exclamation_label.grid(row=4, column=2)

        self.warning_label = Label(self.center_frame, text="", font=("Helvetica", 15), fg=self.error_color)
        self.warning_label.grid(row=5, columnspan=2, padx=5)

        empty_space = Label(self.center_frame, text='\n')
        empty_space.grid(row=6, column=1)

        change_password_button = customtkinter.CTkButton(self.center_frame, text="Change Password", font=("Helvetica", 18), command=self.change_password, width=180, height=40)
        change_password_button.grid(row=10, columnspan=2, pady=5)

        login_button = customtkinter.CTkButton(self.center_frame, text="Log In", font=("Helvetica", 18), command=self.launch_login_page, width=180, height=40)
        login_button.grid(row=11, columnspan=2, pady=5)

        self.success_message = Label(self.center_frame, text="", font=("Helvetica", 18), fg="green")
        self.success_message.grid(row=12, columnspan=2)

        self.password_1_value = None 
        self.password_2_value = None 

        # Center widgets
        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def change_password(self):
        if not self.validate_password():
           return

        new_password_hashed = hashlib.md5(self.password_2_value.encode('utf-8')).hexdigest().upper() # type: ignore
        self.db.update_password(self.uid, new_password_hashed)
        self.success_message.config(text="\nPassword changed successfully!")


    def validate_password(self):
        self.password_1_value = self.password_1_entry.get()
        self.password_2_value = self.password_2_entry.get() 
        self.verification_code_value = self.verification_code_entry.get()

        self.verification_code_exclamation_label.config(text="")
        self.repeat_password_exclamation_label.config(text="")
        self.password_exclamation_label.config(text="")
        self.warning_label.config(text="")
        ok_flag = True 
        error_message = ""

        minimum_password_length = 8
        letters = 'qwertyuiopasdfghjklzxcvbnm'
        digits = '0123456789'
        special_characters = '~!@#$%^&*.'

        if not self.verification_code_value:
            ok_flag = False
            self.verification_code_exclamation_label.config(text="!")

        if not self.password_1_value:
            ok_flag = False
            self.password_exclamation_label.config(text="!")

        if not self.password_2_value:
            ok_flag = False
            self.repeat_password_exclamation_label.config(text="!")

        if self.verification_code_value and self.verification_code_value != str(self.verification_code):
            ok_flag = False
            self.verification_code_exclamation_label.config(text="!")
            error_message = error_message + "Incorrect verification code\n"

        if self.password_1_value:
            if not len(self.password_1_value) >= minimum_password_length:
                ok_flag = False
                self.password_exclamation_label.config(text="!")
                error_message = error_message + "Password should be at least 8 characters long.\n"

            if not any(c in letters for c in self.password_1_value):
                ok_flag = False
                self.password_exclamation_label.config(text="!")
                error_message = error_message + "Password should contain at least one lower-case letter.\n"

            if not any(c in letters.upper() for c in self.password_1_value):
                ok_flag = False
                self.password_exclamation_label.config(text="!")
                error_message = error_message + "Password should contain at least one upper-case letter.\n"

            if not any(c in digits for c in self.password_1_value):
                ok_flag = False
                self.password_exclamation_label.config(text="!")
                error_message = error_message + "Password should contain at least one digit.\n"

            if not any(c in special_characters for c in self.password_1_value):
                ok_flag = False
                self.password_exclamation_label.config(text="!")
                error_message = error_message + f"Password should contain at least one \n special character: {special_characters}\n"

        if self.password_2_value and self.password_1_value != self.password_2_value:
            ok_flag = False
            self.repeat_password_exclamation_label.config(text="!")
            error_message = error_message + "Passwords do not match.\n"

        if error_message or not ok_flag:
            self.warning_label.config(text=error_message)
        
        return ok_flag


    def launch_login_page(self):
        login_page_frame = login_page.LoginPage(parent=self.parent, db=self.db)
        login_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        login_page_frame.tkraise()

