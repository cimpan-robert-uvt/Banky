import hashlib
import customtkinter
import tkinter
import home_page


class AccountsPage(tkinter.Frame):
    def __init__(self, parent, db, user):
        super().__init__(parent)
        self.error_color = "#f75002"
        self.parent = parent
        self.db = db
        self.user = user
        self.uid = db.get_uid(self.user)

        self.entry_list = []
        self.entry_warning_dict = dict()

        self.center_frame = tkinter.Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tkinter.Label(self.center_frame, text="\n\nManage Accounts\n\n", font=("Helvetica", 24))
        title.grid(row=0, columnspan=2)

        text_label = tkinter.Label(self.center_frame, text="Enter currency for the account you want to delete: ", font=("Helvetica", 13))
        text_label.grid(row=1, column=0, pady=10, padx=10)

        self.currency_entry = tkinter.Entry(self.center_frame, font=("Helvetica", 18), width=7)
        self.currency_entry.grid(row=1, column=1, pady=10, padx=10)

        self.warning_label = tkinter.Label(self.center_frame, text="", font=("Helvetica", 13), fg=self.error_color)
        self.warning_label.grid(row=1, column=2)

        password_label = tkinter.Label(self.center_frame, text="Enter password: ", font=("Helvetica", 13))
        password_label.grid(row=2, column=0, pady=10, padx=10)

        self.password_entry = tkinter.Entry(self.center_frame, show="*", font=("Helvetica", 18), width=7)
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)

        self.warning_password = tkinter.Label(self.center_frame, text="", font=("Helvetica", 13), fg=self.error_color)
        self.warning_password.grid(row=2, column=2)

        space_label = tkinter.Label(self.center_frame, text="\n\n", font=("Helvetica", 18))
        space_label.grid(row=4, columnspan=2, pady=5, padx = 5)

        self.check_var = tkinter.StringVar()

        self.checkbox = customtkinter.CTkCheckBox(self.center_frame, text="I acknowledge that the account will be deleted and cannot be recovered.", variable=self.check_var, onvalue="on", offvalue="off", text_color="black")
        self.checkbox.grid(row=5, column=0, columnspan=2, pady=5, padx = 5)
        
        self.warning_checkbox = tkinter.Label(self.center_frame, text="", font=("Helvetica", 13), fg=self.error_color)
        self.warning_checkbox.grid(row=5, column=2)

        self.warning_main_account = tkinter.Label(self.center_frame, text="", font=("Helvetica", 13), fg=self.error_color)
        self.warning_main_account.grid(row=6, column=0,columnspan=2, pady=10, padx=10)
      
        space_label = tkinter.Label(self.center_frame, text="\n\n", font=("Helvetica", 18))
        space_label.grid(row=7, columnspan=2, pady=5, padx = 5)

        delete_account_button = customtkinter.CTkButton(self.center_frame, text="Delete Account", font=("Helvetica", 18), command=self.process_delete_account, width=180, height=40)
        delete_account_button.grid(row=8,  columnspan=2, pady=5, padx=5)

        home_button = customtkinter.CTkButton(self.center_frame, text="Home Page", font=("Helvetica", 18), command=self.launch_home_page, width=180, height=40)
        home_button.grid(row=9, columnspan=2, pady=5)

        self.pack_widgets()


    def pack_widgets(self):
        for widget in self.winfo_children():
            widget.pack_configure(expand=True, anchor='center')


    def process_delete_account(self):
        self.currency = self.currency_entry.get()
        self.password_value = self.password_entry.get()
        self.hashed_password = hashlib.md5(self.password_value.encode('utf-8')).hexdigest().upper()
        self.email = self.db.get_email(self.uid)

        self.warning_label.config(text="")
        self.warning_password.config(text="")
        self.warning_checkbox.config(text="")
        self.warning_main_account.config(text="")

        ok_flag = True

        if not self.check_var.get() or self.check_var.get() == "off":
            ok_flag = False
            self.warning_checkbox.config(text="!")

        if not self.currency_entry or self.currency not in self.db.get_currencies_for_user(self.uid):
            ok_flag = False
            self.warning_label.config(text="!")
            self.checkbox.deselect()

        if not self.password_value or not self.db.check_if_password_is_correct(self.email, self.hashed_password):
            ok_flag = False
            self.warning_password.config(text="!")
            self.checkbox.deselect()

        if self.currency == self.db.get_main_account_currency(self.db.get_email(self.uid))[0]:
            ok_flag = False
            self.warning_main_account.config(text="You cannot delete the main account, you need to contact the bank.")

        else:
            account_balance = float(self.db.get_ammount_for_account(self.uid, self.currency))
            if account_balance > 0.0:
                ok_flag = False
                self.warning_main_account.config(text=f"Cannot delete account with positive balance: {account_balance}")

        if not ok_flag:
            return
        
        self.db.delete_account(self.uid, self.currency)
        self.warning_main_account.config(fg="green", text=f"Successfully deleted {self.currency} account.")


    def launch_home_page(self):
        home_page_frame = home_page.HomePage(self.parent, user=self.user, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()

