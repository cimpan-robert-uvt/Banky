import customtkinter
import hashlib
import home_page
import re

from datetime import datetime
from tkinter import * # type: ignore
from utils import CURRENCIES, AMOUNT_REGEX_PATTERN


class AddMoneyPage(Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.user = user
        self.uid = db.get_uid(self.user)
        self.error_color = "#f75002"

        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = Label(self.center_frame, text="\nAdd Money\n\n", font=("Helvetica", 24))
        label.grid(row=0, columnspan=3, pady=10, padx=5)

        label = Label(self.center_frame, text="Amount: ", font=("Helvetica", 24))
        label.grid(row=1, column=0, pady=5)

        self.ammount_entry = Entry(self.center_frame, font=("Helvetica", 18), width=13)
        self.ammount_entry.grid(row=1, column=1, pady=5)

        self.currency_menu = customtkinter.CTkOptionMenu(self.center_frame, dropdown_fg_color="white", dropdown_text_color="black", values=CURRENCIES)
        self.currency_menu.grid(row=1, column=2)
        self.currency_menu.set(self.db.get_main_account_currency(self.user))

        label = Label(self.center_frame, text="Source: ", font=("Helvetica", 24))
        label.grid(row=2, column=0, pady=5)

        self.from_account_entry = Entry(self.center_frame, font=("Helvetica", 18), width=24)
        self.from_account_entry.grid(row=2,column = 1,  columnspan=2, pady=5)

        space = Label(self.center_frame, text='\n\n')
        space.grid(row=3, columnspan=3)

        add_button = customtkinter.CTkButton(self.center_frame, text="Add", font=("Helvetica", 18), command=self.add_money, width=180, height=40)
        add_button.grid(row=6, columnspan=3, pady=10, padx=5)

        home_button = customtkinter.CTkButton(self.center_frame, text="Back", font=("Helvetica", 18), command=self.launch_home_page, width=180, height=40)
        home_button.grid(row=7,columnspan=3, pady=10, padx=5)

        space = Label(self.center_frame, text='\n\n')
        space.grid(row=8, columnspan=3)

        self.message_label = Label(self.center_frame, text="", font=("Helvetica", 24))
        self.message_label.grid(row=10, columnspan=3)

        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def add_money(self):
        amount = self.ammount_entry.get()
        currency = self.currency_menu.get()

        self.message_label.config(text="")

        if not re.match(AMOUNT_REGEX_PATTERN, amount) or not amount:
            self.message_label.config(fg=self.error_color, text="\nInvalid format or empty amount.")
            return
        
        if amount:
            amount = round(float(amount.replace(",",".")),2)

        if isinstance(currency, tuple):
            currency = currency[0]

        if not self.db.check_if_account_exists_for_currency(self.uid, currency):
            self.db.create_account_for_currency(self.uid, currency, amount)
        else:
            self.db.add_ammount_for_existing_account(self.uid, currency, amount)

        user_account = self.db.get_account_id(self.uid, currency)
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = hashlib.md5((user_account + str(now)).encode('utf-8')).hexdigest().upper()

        transaction_params = (transaction_id, "top-up", self.uid, self.uid, self.from_account_entry.get(), user_account, amount, currency, amount, currency, now)
        self.db.add_transaction(transaction_params)

        self.db.get_all_from_db()

        self.message_label.config(fg="green", text=f"Successfully added {amount} {currency}.")


    def launch_home_page(self):
        home_page_frame = home_page.HomePage(self.parent, user=self.user, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()

