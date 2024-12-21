import customtkinter
import tkinter as tk
import hashlib
import re
import start_page

from datetime import datetime
from home_page import HomePage
from utils import CURRENCIES, send_mail


class CreateAccountPage(tk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.error_color = "#f75002"
        self.parent = parent
        self.db = db

        self.entry_list = []
        self.entry_warning_dict = dict()

        self.center_frame = tk.Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(self.center_frame, text="\nCreate Account", font=("Helvetica", 24))
        title.grid(row=0, column=1)

        empty_space = tk.Label(self.center_frame, text='\n')
        empty_space.grid(row=1, column=1)

        # --------------
        #   First Name
        # --------------
        first_name_label = tk.Label(self.center_frame, text="First Name:", font=("Helvetica", 18))
        first_name_label.grid(row=2, column=1)

        self.first_name_entry = tk.Entry(self.center_frame, font=("Helvetica", 18), width=40)
        self.first_name_entry.grid(row=3, column=1, pady=5)
        self.entry_list.append(self.first_name_entry)

        first_name_exclamation_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        first_name_exclamation_label.grid(row=3, column=2, padx=5)

        self.entry_warning_dict[self.first_name_entry] = first_name_exclamation_label

        # --------------
        #   Last Name
        # --------------
        last_name_label = tk.Label(self.center_frame, text="Last Name:", font=("Helvetica", 18))
        last_name_label.grid(row=4, column=1)

        self.last_name_entry = tk.Entry(self.center_frame, font=("Helvetica", 18), width=40)
        self.last_name_entry.grid(row=5, column=1, pady=5)
        self.entry_list.append(self.last_name_entry)

        last_name_exclamation_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        last_name_exclamation_label.grid(row=5, column=2, padx=5)

        self.entry_warning_dict[self.last_name_entry] = last_name_exclamation_label

        # --------------
        #   Email
        # --------------
        email_label = tk.Label(self.center_frame, text="Email:", font=("Helvetica", 18))
        email_label.grid(row=6, column=1)

        self.email_entry = tk.Entry(self.center_frame, font=("Helvetica", 18), width=40)
        self.email_entry.grid(row=7, column=1, pady=5)
        self.entry_list.append(self.email_entry)

        email_exclamation_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        email_exclamation_label.grid(row=7, column=2, padx=5)

        self.entry_warning_dict[self.email_entry] = email_exclamation_label

        # ----------------
        #   Phone Number
        # ----------------
        phone_label = tk.Label(self.center_frame, text="Phone Number:", font=("Helvetica", 18))
        phone_label.grid(row=8, column=1)

        self.phone_entry = tk.Entry(self.center_frame, font=("Helvetica", 18), width=40)
        self.phone_entry.grid(row=9, column=1, pady=5)
        self.entry_list.append(self.phone_entry)

        phone_exclamation_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        phone_exclamation_label.grid(row=9, column=2, padx=5)
        self.entry_warning_dict[self.phone_entry] = phone_exclamation_label

        # --------------
        #   Password
        # --------------
        password_1_label = tk.Label(self.center_frame, text="Password:", font=("Helvetica", 18))
        password_1_label.grid(row=10, column=1)

        self.password_1_entry = tk.Entry(self.center_frame, show="*", font=("Helvetica", 18), width=40)
        self.password_1_entry.grid(row=11, column=1, pady=5)
        self.entry_list.append(self.password_1_entry)

        password_exclamation_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        password_exclamation_label.grid(row=11, column=2, padx=5)

        self.entry_warning_dict[self.password_1_entry] = password_exclamation_label

        # -------------------
        #   Repeat Password
        # -------------------
        password_2_label = tk.Label(self.center_frame, text="Repeat Password:", font=("Helvetica", 18))
        password_2_label.grid(row=12, column=1)

        self.password_2_entry = tk.Entry(self.center_frame, show="*", font=("Helvetica", 18), width=40)
        self.password_2_entry.grid(row=13, column=1, pady=10)
        self.entry_list.append(self.password_2_entry)

        repeat_password_exclamation_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        repeat_password_exclamation_label.grid(row=13, column=2, padx=5)

        self.entry_warning_dict[self.password_2_entry] = repeat_password_exclamation_label

        # ------------------------------
        #   Main currency option menu
        # ------------------------------

        self.currency_menu = customtkinter.CTkOptionMenu(self.center_frame, values=CURRENCIES, dropdown_fg_color="white", dropdown_text_color="black")
        self.currency_menu.grid(row=14, column=1, pady=5, padx=10)
        self.currency_menu.set("EUR")  # set initial value

        # ------------------
        #   Warning message
        # ------------------
        self.error_label = tk.Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.error_label.grid(row=15, column=1, pady=5, padx=10)

        # ------------------
        #      Buttons
        # ------------------
        create_account_button = customtkinter.CTkButton(self.center_frame, text="Create Account", font=("Helvetica", 18), command=self.create_account, width=180, height=40)
        create_account_button.grid(row=16, column=1, pady=5, padx=5)

        start_button = customtkinter.CTkButton(self.center_frame, text="Start Page", font=("Helvetica", 18), command=self.launch_start_page, width=180, height=40)
        start_button.grid(row=17, column=1, pady=5)

        # Declaring class attributes as none , they will be assigned a value after the user clicks the Create Account button

        self.uid = None
        self.account_id = None
        self.hashed_password = None
        self.phone_value = None
        self.first_name_value = None
        self.last_name_value = None
        self.email_value = None
        self.password_1_value = None
        self.password_2_value = None
        self.account_creation_date = None
        self.currency_value = None

        for e in self.entry_list:
            self.entry_warning_dict[e].config(text="*")

        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def create_account(self):
        if not self.validate_user_input():
            return

        # Hash password before storing in db
        self.hashed_password = hashlib.md5(self.password_2_value.encode('utf-8')).hexdigest().upper() # type: ignore

        # Generate unique id that will be primary key in the table 'clients'
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        hashed_value = hashlib.md5((self.email_value + str(now)).encode('utf-8')).hexdigest().upper() # type: ignore
        self.uid = hashed_value
        self.account_id = "BANKY" + hashlib.md5((self.email_value + str(now)).encode('utf-8')).hexdigest().upper() + self.currency_value # type: ignore
        self.account_creation_date = datetime.now()

        client_params = (self.uid, self.first_name_value, self.last_name_value, self.email_value, self.hashed_password, self.phone_value, self.currency_value, self.account_id)
        account_params = (self.account_id, self.uid, self.currency_value, 0.0, self.account_creation_date)

        self.db.add_client_to_db(client_params)
        self.db.add_account_to_db(account_params)

        send_mail(self.email_value, "Thank you for registering!", "Hello, \nWelcome to Banky!")

        home_page_frame = HomePage(self.parent, user=self.email_value, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()
        return


    def validate_user_input(self):
        self.first_name_value = self.first_name_entry.get()
        self.last_name_value = self.last_name_entry.get()
        self.password_1_value = self.password_1_entry.get()
        self.password_2_value = self.password_2_entry.get()
        self.email_value = self.email_entry.get()
        self.phone_value = self.phone_entry.get()
        self.currency_value = self.currency_menu.get()

        self.error_label.config(text="")
        self.first_name_entry.config(fg="black")
        self.last_name_entry.config(fg="black")
        self.email_entry.config(fg="black")
        self.password_1_entry.config(fg="black")
        self.password_2_entry.config(fg="black")
        self.phone_entry.config(fg="black")

        ok_flag = True
        error_message = ""

        for e in self.entry_list:
            if e.get():
                self.entry_warning_dict[e].config(text="")
            else:
                ok_flag = False

        if self.first_name_value and not all(c.isalpha() or c.isspace() for c in self.first_name_value):
            ok_flag = False
            self.first_name_entry.config(fg=self.error_color)
            error_message = error_message + "First name must contain only letters.\n"
            self.entry_warning_dict[self.first_name_entry].config(text="!")

        if self.last_name_value and not all(c.isalpha() or c.isspace() for c in self.last_name_value):
            ok_flag = False
            self.last_name_entry.config(fg=self.error_color)
            self.entry_warning_dict[self.last_name_entry].config(text="!")
            error_message = error_message + "Last name must contain only letters.\n"

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if self.email_value and not re.match(email_pattern, self.email_value):
            ok_flag = False
            self.email_entry.config(fg=self.error_color)
            self.entry_warning_dict[self.email_entry].config(text="!")
            error_message = error_message + "Invalid email format.\n"

        if self.email_value and self.db.check_if_user_exists(self.email_value):
            ok_flag = False
            self.email_entry.config(fg=self.error_color)
            self.entry_warning_dict[self.email_entry].config(text="!")
            error_message = error_message + "An account already exists with this email address.\n"

        if self.phone_value and not self.phone_value.isdigit():
            ok_flag = False
            self.phone_entry.config(fg=self.error_color)
            self.entry_warning_dict[self.phone_entry].config(text="!")
            error_message = error_message + "Phone number should contain only digits.\n"

        minimum_password_length = 8
        letters = 'qwertyuiopasdfghjklzxcvbnm'
        digits = '0123456789'
        special_characters = '~!@#$%^&*.'

        if self.password_1_value:

            if not len(self.password_1_value) >= minimum_password_length:
                ok_flag = False
                self.password_1_entry.config(fg=self.error_color)
                self.entry_warning_dict[self.password_1_entry].config(text="!")
                error_message = error_message + "Password should be at least 8 characters long.\n"

            if not any(c in letters for c in self.password_1_value):
                ok_flag = False
                self.password_1_entry.config(fg=self.error_color)
                self.entry_warning_dict[self.password_1_entry].config(text="!")
                error_message = error_message + "Password should contain at least one lower-case letter.\n"

            if not any(c in letters.upper() for c in self.password_1_value):
                ok_flag = False
                self.password_1_entry.config(fg=self.error_color)
                self.entry_warning_dict[self.password_1_entry].config(text="!")
                error_message = error_message + "Password should contain at least one upper-case letter.\n"

            if not any(c in digits for c in self.password_1_value):
                ok_flag = False
                self.password_1_entry.config(fg=self.error_color)
                self.entry_warning_dict[self.password_1_entry].config(text="!")
                error_message = error_message + "Password should contain at least one digit.\n"

            if not any(c in special_characters for c in self.password_1_value):
                ok_flag = False
                self.password_1_entry.config(fg=self.error_color)
                self.entry_warning_dict[self.password_1_entry].config(text="!")
                error_message = error_message + f"Password should contain at least one \n special character: {special_characters}\n"

        if self.password_2_value and self.password_1_value != self.password_2_value:
            ok_flag = False
            self.password_2_entry.config(fg=self.error_color)
            self.entry_warning_dict[self.password_2_entry].config(text="!")
            error_message = error_message + "Passwords do not match.\n"

        if error_message or not ok_flag:
            self.error_label.config(text=error_message)

        return ok_flag


    def launch_start_page(self):
        start_page_frame = start_page.StartPage(parent=self.parent, db=self.db)
        start_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        start_page_frame.tkraise()

