import customtkinter
import start_page
import add_money_page
import transfer_page
import exchange_page
import transactions_page
import accounts_page

from tkinter import * # type: ignore


class HomePage(Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.parent = parent
        self.db = db
        self.uid = self.db.get_uid(self.user)

        #self.db.get_all_from_db()

        self.center_frame = Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = Label(self.center_frame, text="\nHome Page\n\n", font=("Helvetica", 24))
        label.grid(row=0, columnspan=2)

        self.currency_menu = customtkinter.CTkOptionMenu(self.center_frame, dropdown_fg_color="white", dropdown_text_color="black", values=self.db.get_currencies_for_user(self.uid), command=self.update_displayed_ammount)
        self.currency_menu.grid(row=1, column=1)
        self.currency_menu.set(self.db.get_main_account_currency(self.user))  # set initial value

        self.ammount_label = Label(self.center_frame, text=self.db.get_ammount_for_account(self.uid, self.currency_menu.get()), font=("Helvetica", 18))
        self.ammount_label.grid(row=1, column=0)

        space = Label(self.center_frame, text="\n\n\n", font=("Helvetica", 24))
        space.grid(row=2, columnspan=2)

        add_money_button = customtkinter.CTkButton(self.center_frame, text="Add money", font=("Helvetica", 18), command=self.launch_add_money_page, width=180, height=40)
        add_money_button.grid(row=3, column=0, pady=10, padx=5)

        make_transfer_button = customtkinter.CTkButton(self.center_frame, text="Make Transfer", font=("Helvetica", 18), command=self.launch_transfer_page, width=180, height=40)
        make_transfer_button.grid(row=3, column=1, pady=10, padx=5)

        exchange_button = customtkinter.CTkButton(self.center_frame, text="Exchange", font=("Helvetica", 18), command=self.launch_exchange_page, width=180, height=40)
        exchange_button.grid(row=4, column=0, pady=10, padx=5)

        transactions_button = customtkinter.CTkButton(self.center_frame, text="Transactions", font=("Helvetica", 18), command=self.launch_transactions_page, width=180, height=40)
        transactions_button.grid(row=4, column=1, pady=10, padx=5)

        accounts_button = customtkinter.CTkButton(self.center_frame, text="Accounts", font=("Helvetica", 18), command=self.launch_accounts_page, width=180, height=40)
        accounts_button.grid(row=5, column=0, pady=10, padx=5)
        
        logout_button = customtkinter.CTkButton(self.center_frame, text="Log out", font=("Helvetica", 18), command=self.logout, width=180, height=40)
        logout_button.grid(row=5, column=1, pady=10, padx=5)

        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def update_displayed_ammount(self, choice):
        self.ammount_label.config(text=self.db.get_ammount_for_account(self.uid, choice))


    def launch_add_money_page(self):
        add_money_page_frame = add_money_page.AddMoneyPage(self.parent, user=self.user, db=self.db)
        add_money_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        add_money_page_frame.tkraise()


    def launch_transfer_page(self):
        transfer_page_frame = transfer_page.TransferPage(self.parent, user=self.user, db=self.db)
        transfer_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        transfer_page_frame.tkraise()


    def launch_exchange_page(self):
        exchange_page_frame = exchange_page.ExchangePage(self.parent, user=self.user, db=self.db)
        exchange_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        exchange_page_frame.tkraise()


    def launch_transactions_page(self):
        transaction_page_frame = transactions_page.TransactionsPage(self.parent, user=self.user, db=self.db)
        transaction_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        transaction_page_frame.tkraise()


    def launch_accounts_page(self):
        accounts_page_frame = accounts_page.AccountsPage(self.parent, db=self.db, user = self.user)
        accounts_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        accounts_page_frame.tkraise()


    def logout(self):
        start_page_frame = start_page.StartPage(self.parent, db=self.db)
        start_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        start_page_frame.tkraise()

