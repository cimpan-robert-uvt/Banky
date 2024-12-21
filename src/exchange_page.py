import customtkinter
import hashlib
import re
import home_page

from tkinter import * # type: ignore
from PIL import Image, ImageTk
from datetime import datetime
from utils import CURRENCIES, AMOUNT_REGEX_PATTERN, exchange


class ExchangePage(Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.user = user
        self.uid = db.get_uid(self.user)
        self.error_color = "#f75002"

        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = Label(self.center_frame, text="\nExchange\n\n", font=("Helvetica", 24))
        label.grid(row=0, columnspan=3, pady=10, padx=5)

        self.currency_menu_from = customtkinter.CTkOptionMenu(self.center_frame, dropdown_fg_color="white", dropdown_text_color="black", values=self.db.get_currencies_for_user(self.uid), command=self.update_displayed_ammount_from)
        self.currency_menu_from.grid(row=1, column=0, pady=10, padx=10)
        self.currency_menu_from.set(self.db.get_main_account_currency(self.user))

        self.my_variable = StringVar()
        self.my_variable.trace_variable("w", self.trace_when_Entry_widget_is_updated)

        self.ammount_entry = Entry(self.center_frame, textvariable = self.my_variable, font=("Helvetica", 18), width=10)
        self.ammount_entry.grid(row=1, column=1, pady=10, padx=10)

        self.label_warning = Label(self.center_frame, text="", font=("Helvetica", 12), fg=self.error_color)
        self.label_warning.grid(row=1, column=2, pady=5)

        self.label_from = Label(self.center_frame, text=f"Balance: {self.db.get_ammount_for_account(self.uid, self.db.get_main_account_currency(self.user))}", font=("Helvetica", 12))
        self.label_from.grid(row=2, column=0, pady=5)

        self.balance_warning = Label(self.center_frame, text="", font=("Helvetica", 12), fg=self.error_color)
        self.balance_warning.grid(row=2, column=1, pady=5)

        image_path = "arrow_down.png"  # Replace with your image path
        image = Image.open(image_path)
        image = image.resize((45, 45))
        photo = ImageTk.PhotoImage(image)

        image_label = Label(self.center_frame, image=photo)
        image_label.image = photo  # type: ignore # This line keeps a reference to the image to prevent it from being garbage collected
        image_label.grid(row=3, columnspan=2)

        self.currency_menu_to = customtkinter.CTkOptionMenu(self.center_frame, dropdown_fg_color="white", dropdown_text_color="black", values=CURRENCIES, command=self.update_displayed_ammount_to)
        self.currency_menu_to.grid(row=4, column=0, pady=10, padx=10)
        self.currency_menu_to.set("RON")

        self.label_exchange = Label(self.center_frame, font=("Helvetica", 18))
        self.label_exchange.grid(row=4, column=1, pady=5)

        self.label_to = Label(self.center_frame, text=f"Balance: {self.db.get_ammount_for_account(self.uid, 'RON')}", font=("Helvetica", 12))
        self.label_to.grid(row=5, column=0, pady=5)

        space_label = Label(self.center_frame, text="\n\n", font=("Helvetica", 18))
        space_label.grid(row=6, pady=5, padx = 5)

        self.currency_warning = Label(self.center_frame, text="", font=("Helvetica", 18), fg=self.error_color)
        self.currency_warning.grid(row=7, columnspan=3, pady=10)

        exchange_button = customtkinter.CTkButton(self.center_frame, text="Exchange", font=("Helvetica", 18), command=self.process_exchange, width=180, height=40)
        exchange_button.grid(row=8, columnspan=3, pady=10, padx=5)

        home_button = customtkinter.CTkButton(self.center_frame, text="Back", font=("Helvetica", 18), command=self.launch_home_page, width=180, height=40)
        home_button.grid(row=9, columnspan=3 , pady=10, padx=5)

        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def update_displayed_ammount_from(self, choice):
        new_value = "Balance: " + str(self.db.get_ammount_for_account(self.uid, choice))
        self.label_from.config(text=new_value)
        self.trace_when_Entry_widget_is_updated(None,None,None)


    def update_displayed_ammount_to(self, choice):
        new_value = "Balance: " + str(self.db.get_ammount_for_account(self.uid, choice))
        self.label_to.config(text=new_value)
        self.trace_when_Entry_widget_is_updated(None,None,None)


    def trace_when_Entry_widget_is_updated(self, var, index, mode):
        self.balance_warning.config(text="")
        my_var = self.my_variable.get()
        if not re.match(AMOUNT_REGEX_PATTERN, my_var) and my_var:
            self.balance_warning.config(text="Invalid format.")
            self.label_exchange.config(text="")
            return
        self.label_exchange.config(text = exchange(self.currency_menu_from.get(), self.currency_menu_to.get(), self.clean_input_amount(my_var)))


    def process_exchange(self):
        currency_from = self.currency_menu_from.get()
        amount_from = self.clean_input_amount(self.ammount_entry.get())
        currency_to = self.currency_menu_to.get()
        amount_to = self.label_exchange['text']

        if amount_from:
            amount_from = round(float(self.clean_input_amount(self.ammount_entry.get())), 2)
        else:
            return

        if amount_to:
            amount_to = round(float(self.label_exchange['text']),2)
        else:
            return

        if isinstance(currency_from, tuple):
            currency_from = currency_from[0]

        if isinstance(currency_to, tuple):
            currency_to = currency_to[0]

        self.label_warning.config(text="")

        if amount_from > float(self.db.get_ammount_for_account(self.uid, currency_from)):
            self.label_warning.config(text="!")
            self.balance_warning.config(text = "Amount exceeds balance!")
            return
        
        if currency_from == currency_to:
            self.currency_warning.config(text="You cannot exchange into\nthe same currency!")
            return

        # modif db
        if not self.db.check_if_account_exists_for_currency(self.uid, currency_to):
            self.db.create_account_for_currency(self.uid, currency_to, amount_to)
            self.db.update_ammount_for_existing_account(self.uid, currency_from, amount_from)

        else:
            self.db.transfer_money(self.db.get_account_id(self.uid, currency_from), self.db.get_account_id(self.uid, currency_to), amount_from, amount_to)

        # add transaction
        user_account_from = self.db.get_account_id(self.uid, currency_from)
        user_account_to = self.db.get_account_id(self.uid, currency_to)

        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        transaction_id = hashlib.md5((user_account_from + user_account_to + str(now)).encode('utf-8')).hexdigest().upper()

        transaction_params = (transaction_id, "exchange", self.uid, self.uid, user_account_from, user_account_to, amount_from, currency_from, amount_to, currency_to, now)
        self.db.add_transaction(transaction_params)

        self.db.get_all_from_db()

        # back home
        self.launch_home_page()


    def clean_input_amount(self, input_amount):
        if input_amount and input_amount[-1] in (',', '.'):
            input_amount = input_amount[:-1]
        return input_amount.replace(",",".")


    def launch_home_page(self):
        home_page_frame = home_page.HomePage(self.parent, user=self.user, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()

