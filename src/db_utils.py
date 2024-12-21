import sqlite3

from datetime import datetime


class DB():
    def __init__(self):
        self.conn = sqlite3.connect("banky_database.db")
        self.cursor = self.conn.cursor()


    def check_if_user_exists(self, email):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients
            (uid TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, email_address TEXT, hashed_password TEXT, phone_number TEXT, main_account_currency TEXT, main_account_id TEXT)
            """)

        data = self.cursor.execute(f"SELECT * FROM clients where email_address = '{email}'").fetchall()
        if not data:
            return False
        else:
            return True


    def check_if_password_is_correct(self, email, password):
        data = self.cursor.execute(f"SELECT * FROM clients where email_address = '{email}' and hashed_password = '{password}'").fetchall()

        if not data:
            return False
        else:
            return True


    def add_client_to_db(self, client_params):
        self.cursor.execute(
            f"INSERT INTO clients (uid, first_name, last_name, email_address, hashed_password, phone_number, main_account_currency, main_account_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            client_params
        )

        self.conn.commit()


    def add_account_to_db(self, account_params):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts
            (account_id TEXT PRIMARY KEY, uid TEXT, currency TEXT, ammount TEXT, account_creation_date TEXT)
            """)

        self.cursor.execute(
            f"INSERT INTO accounts (account_id, uid, currency, ammount, account_creation_date) VALUES (?, ?, ?, ?, ?)",
            account_params
        )

        self.conn.commit()


    def get_main_account_currency(self, email):
        data = self.cursor.execute(f"SELECT main_account_currency FROM clients where email_address = '{email}'").fetchall()
        return data[0]


    def get_main_account_id(self, email):
        data = self.cursor.execute(f"SELECT main_account_id FROM clients where email_address = '{email}'").fetchall()
        return data[0]


    def get_ammount_for_account(self, uid, currency):
        if isinstance(currency, tuple):
            currency = currency[0]
        data = self.cursor.execute(f"SELECT ammount FROM accounts where uid = '{uid}' and currency = '{currency}'").fetchall()

        if not data:
            return 0.0

        return data[0][0]


    def get_currencies_for_user(self, uid):
        data = self.cursor.execute(f"SELECT DISTINCT currency FROM accounts where uid = '{uid}'").fetchall()
        currency_list = [t[0] for t in data]
        return currency_list


    def get_all_from_db(self):
        data1 = self.cursor.execute(f"SELECT * FROM clients").fetchall()
        data2 = self.cursor.execute(f"SELECT * FROM accounts ").fetchall()
        data3 = self.cursor.execute(f"SELECT * FROM transactions ").fetchall()

        print('__________________________________________________')
        for tup in data1:
            print(tup)
        print('__________________________________________________')
        for tup in data2:
            print(tup)
        print('__________________________________________________')
        for tup in data3:
            print(tup)
        print('__________________________________________________')


    def check_if_account_exists_for_currency(self, uid, currency):
        if isinstance(currency, tuple):
            currency = currency[0]
        data = self.cursor.execute(f"SELECT * FROM accounts where uid = '{uid}' and currency = '{currency}'").fetchall()

        if not data:
            return False
        return True


    def get_uid(self, email):
        uid = self.cursor.execute(f"SELECT uid FROM clients where email_address = '{email}'").fetchall()
        return uid[0][0]


    def get_name(self, uid):
        uid = self.cursor.execute(f"SELECT first_name FROM clients where uid = '{uid}'").fetchall()
        return uid[0][0]
    

    def get_email(self, uid):
        email = self.cursor.execute(f"SELECT email_address FROM clients where uid = '{uid}'").fetchall()
        return email[0][0]


    def create_account_for_currency(self, uid, currency, ammount):
        new_account_id = 'BANKY' + uid + currency
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        account_params = (new_account_id, uid, currency, ammount, now)

        self.cursor.execute(
            "INSERT INTO accounts (account_id, uid, currency, ammount, account_creation_date) VALUES (?, ?, ?, ?, ?)",
            account_params
        )

        self.conn.commit()


    def add_ammount_for_existing_account(self, uid, currency, ammount):
        if isinstance(currency, tuple):
            currency = currency[0]

        current_ammount = self.get_ammount_for_account(uid,currency)
        new_total = float(current_ammount) + float(ammount)
        self.cursor.execute(
            f"UPDATE accounts SET ammount = '{new_total}' WHERE uid = '{uid}' and currency = '{currency}'"
        )

        self.conn.commit()


    def update_ammount_for_existing_account(self, uid, currency, amount):
        current_ammount = self.get_ammount_for_account(uid, currency)
        new_total = round(float(current_ammount) - float(amount),2)
        self.cursor.execute(
            f"UPDATE accounts SET ammount = '{new_total}' WHERE uid = '{uid}' and currency = '{currency}'"
        )

        self.conn.commit()


    def get_user_accounts(self, uid):
        data = self.cursor.execute(f"SELECT DISTINCT account_id FROM accounts where uid = '{uid}'").fetchall()
        accounts_list = [t[0] for t in data]
        return accounts_list


    def get_account_id(self, uid, currency):
        uid = self.cursor.execute(f"SELECT account_id FROM accounts where uid = '{uid}' and currency = '{currency}'").fetchall()
        return uid[0][0]


    def get_uid_from_account(self, account_id):
        uid = self.cursor.execute(f"SELECT distinct uid FROM accounts where account_id = '{account_id}'").fetchall()
        return uid[0][0]

    def add_transaction(self, transaction_params):
        # self.cursor.execute("DROP TABLE transactions")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions
            (transaction_id TEXT PRIMARY KEY, transaction_type TEXT, sender_uid TEXT, receiver_uid TEXT, sender_account_id TEXT, receiver_account_id TEXT, sender_amount TEXT, sender_currency TEXT, receiver_amount TEXT, receiver_currency TEXT, timestamp TEXT)
            """)

        self.cursor.execute(
            f"INSERT INTO transactions (transaction_id, transaction_type, sender_uid, receiver_uid, sender_account_id, receiver_account_id, sender_amount, sender_currency, receiver_amount, receiver_currency, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            transaction_params
        )

        self.conn.commit()

        pass


    def get_amount_for_account_id(self, account_id):
        uid = self.cursor.execute(f"SELECT ammount FROM accounts where account_id = '{account_id}'").fetchall()
        return uid[0][0]


    def transfer_money(self, from_account, to_account, amount_in_sender_currency, amount_in_receiver_currency):
        current_amount_from = self.get_amount_for_account_id(from_account)
        current_amount_to = self.get_amount_for_account_id(to_account)

        new_amount_from = round(float(current_amount_from) - float(amount_in_sender_currency), 2)
        new_amount_to = round(float(current_amount_to) + float(amount_in_receiver_currency), 2)

        self.cursor.execute(
            f"UPDATE accounts SET ammount = '{new_amount_from}' WHERE account_id = '{from_account}'"
        )

        self.cursor.execute(
            f"UPDATE accounts SET ammount = '{new_amount_to}' WHERE account_id = '{to_account}'"
        )

        self.conn.commit()


    def get_transactions(self, uid):
        # top_ups = self.cursor.execute(f"SELECT * FROM transactions where transaction_type = 'top-up' and sender_uid = '{uid}' ").fetchall()
        # exchanges = self.cursor.execute(f"SELECT * FROM transactions where transaction_type = 'exchange' and sender_uid = '{uid}'").fetchall()
        # transfers_from_user = self.cursor.execute(f"SELECT * FROM transactions where transaction_type = 'transfer' and sender_uid = '{uid}'").fetchall()
        # transfers_to_user = self.cursor.execute(f"SELECT * FROM transactions where transaction_type = 'transfer' and receiver_uid = '{uid}'").fetchall()

        transactions = self.cursor.execute(f"SELECT * FROM transactions WHERE receiver_uid = '{uid}' or sender_uid = '{uid}' ORDER BY timestamp desc").fetchall()

        return list(transactions)


    def delete_account(self, uid, currency):
        self.cursor.execute(f"DELETE from accounts WHERE uid = '{uid}' AND currency = '{currency}'")

        self.conn.commit()


    def update_password(self,uid,new_password):
        self.cursor.execute(f"UPDATE clients SET hashed_password = '{new_password}' WHERE uid = '{uid}'")

        self.conn.commit()


    def get_email_from_account(self, account_id):
        data = self.cursor.execute(f"SELECT email_address FROM clients c JOIN accounts a ON c.uid = a.uid WHERE a.account_id = '{account_id}'").fetchall()
        if not data:
            return False
        
        return data[0][0]

