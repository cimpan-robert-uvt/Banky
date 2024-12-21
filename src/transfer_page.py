import customtkinter
import hashlib
import re
import home_page

from datetime import datetime
from tkinter import * # type: ignore
from utils import AMOUNT_REGEX_PATTERN, exchange,  send_mail


class TransferPage(Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.user = user
        self.uid = db.get_uid(self.user)
        self.error_color = "#f75002"

        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = Label(self.center_frame, text="\nMake a transfer\n\n", font=("Helvetica", 24))
        label.grid(row=0, columnspan=2, pady=10, padx=5)

        receiver_name = Label(self.center_frame, text="Receiver name: ", font=("Helvetica", 18))
        receiver_name.grid(row=1, column=0, pady=5, padx = 5)

        self.receiver_name_entry = Entry(self.center_frame, font=("Helvetica", 18), width=24)
        self.receiver_name_entry.grid(row=1, column=1, columnspan=2, pady=5, padx = 5)

        receiver_iban = Label(self.center_frame, text="Receiver IBAN: ", font=("Helvetica", 18))
        receiver_iban.grid(row=2, column=0, pady=5, padx = 5)

        self.receiver_iban_entry = Entry(self.center_frame, font=("Helvetica", 18), width=24)
        self.receiver_iban_entry.grid(row=2, column=1, columnspan=2, pady=5, padx = 5)

        self.receiver_warning = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.receiver_warning.grid(row=2, column=2, pady=5, padx = 5)

        label = Label(self.center_frame, text="Amount: ", font=("Helvetica", 18))
        label.grid(row=3, column=0, pady=5, padx = 5)

        self.amount_entry = Entry(self.center_frame, font=("Helvetica", 18), width=24)
        self.amount_entry.grid(row=3,column = 1, pady=5, padx = 5)

        self.amount_warning = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.amount_warning.grid(row=3, column=2, pady=5, padx = 5)

        label = Label(self.center_frame, text="From account: ", font=("Helvetica", 18))
        label.grid(row=4, column=0, pady=5, padx = 5)

        self.currency_menu = customtkinter.CTkOptionMenu(self.center_frame, dropdown_fg_color="white", dropdown_text_color="black", values=self.db.get_currencies_for_user(self.uid), command=self.update_displayed_ammount)
        self.currency_menu.grid(row=4, column=1, pady=5, padx = 5)
        self.currency_menu.set(self.db.get_main_account_currency(self.user))

        self.balance_label = Label(self.center_frame, text=f"Balance: {self.db.get_ammount_for_account(self.uid, self.currency_menu.get())}", font=("Helvetica", 12))
        self.balance_label.grid(row=5, column=1)
        
        self.warning_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.warning_label.grid(row=6, columnspan=2, pady=5, padx = 5)

        space_label = Label(self.center_frame, text="\n", font=("Helvetica", 18))
        space_label.grid(row=7, columnspan=2, pady=5, padx = 5)

        transfer_button = customtkinter.CTkButton(self.center_frame, text="Transfer", font=("Helvetica", 18), command=self.transfer, width=180, height=40)
        transfer_button.grid(row=8, columnspan=2, pady=5, padx = 5)

        home_button = customtkinter.CTkButton(self.center_frame, text="Home", font=("Helvetica", 18), command=self.launch_home_page, width=180, height=40)
        home_button.grid(row=9, columnspan=2, pady=5, padx = 5)

        space = Label(self.center_frame, text="\n\n", font=("Helvetica", 24))
        space.grid(row=10, columnspan=2)

        self.success_label = Label(self.center_frame, text="", font=("Helvetica", 18), fg="green")
        self.success_label.grid(row=12, columnspan=2)

        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def update_displayed_ammount(self, choice):
        self.balance_label.config(text=self.db.get_ammount_for_account(self.uid, choice))
        self.amount_entry.delete(0, 'end')


    def transfer(self):
        receiver_name = self.receiver_name_entry.get()
        receiver_account = self.receiver_iban_entry.get()
        amount = self.amount_entry.get()
        sender_currency = self.currency_menu.get()
        receiver_currency = receiver_account[-3:]
        receiver_email = self.db.get_email_from_account(receiver_account)

        self.amount_warning.config(text="")
        self.receiver_warning.config(text="")
        self.warning_label.config(text="")

        ok_flag = True
        warning_message = ""

        if not re.match(AMOUNT_REGEX_PATTERN, amount) or not amount:
            self.warning_label.config(text= "\nInvalid format or empty amount.")
            return
            
        # Verificam daca contul caruia trimitem exista in Banky
        if not receiver_email:
            ok_flag = False 
            warning_message = warning_message + "The IBAN doesn't exist.\n" 

        if receiver_account in self.db.get_user_accounts(self.uid):
            self.receiver_warning.config(text="!")
            ok_flag = False

        if amount:
            amount = round(float(amount.replace(",",".")),2)

        if amount and amount > float(self.db.get_ammount_for_account(self.uid, sender_currency)):
            self.amount_warning.config(text="!")
            warning_message = warning_message + "Insufficient funds." 
            ok_flag = False

        if not ok_flag:
            self.warning_label.config(text= warning_message)
            return

        if isinstance(sender_currency, tuple):
            sender_currency = sender_currency[0]

        sender_account = self.db.get_account_id(self.uid,sender_currency )

        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = hashlib.md5((sender_account + receiver_account + str(now)).encode('utf-8')).hexdigest().upper()

        receiver_uid = self.db.get_uid_from_account(receiver_account)

        if sender_currency != receiver_currency:
            # we need to perform an exchange
            amount_in_sender_currency = amount
            amount_in_receiver_currency = exchange(sender_currency,receiver_currency, amount)
            self.db.transfer_money(sender_account, receiver_account, amount_in_sender_currency, amount_in_receiver_currency)
            transaction_params = (transaction_id, "transfer", self.uid, receiver_uid, sender_account, receiver_account, amount_in_sender_currency, sender_currency, amount_in_receiver_currency, receiver_currency, now)
            send_mail(receiver_email, "You got a new transfer!", f"Hello, \nYou received {amount_in_receiver_currency} {receiver_currency} from {self.db.get_name(self.uid)}.")

        else:
            self.db.transfer_money(sender_account, receiver_account, amount, amount)
            transaction_params = (transaction_id, "transfer", self.uid, receiver_uid, sender_account, receiver_account, amount, sender_currency, amount, sender_currency, now)
            send_mail(receiver_email, "You got a new transfer!", f"Hello, \nYou received {amount} {receiver_currency} from {self.db.get_name(self.uid)}.")
        
        self.db.add_transaction(transaction_params)
        self.balance_label.config(text=f"Balance: {self.db.get_ammount_for_account(self.uid, sender_currency)}")

        self.success_label.config(text=f"Successfully transfered {amount} {sender_currency} to {receiver_name}!")

        # self.db.get_all_from_db()


    def launch_home_page(self):
        home_page_frame = home_page.HomePage(self.parent, user=self.user, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()

