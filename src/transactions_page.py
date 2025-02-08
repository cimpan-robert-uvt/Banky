import customtkinter
import home_page
import io

from tkinter import * # type: ignore
from CTkListbox import * # type: ignore

from datetime import datetime
from fpdf import FPDF
from utils import send_mail_with_pdf

class TransactionsPage(Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.user = user
        self.uid = db.get_uid(self.user)
        self.transactions = sorted(self.db.get_transactions(self.uid), key=lambda x: x[10], reverse=True)

        # self.center_frame = Frame(self)
        # self.place(anchor="center")

        label = Label(self, text="\nTransactions History\n", font=("Helvetica", 24))
        label.grid(row=0, pady=10, padx=5)

        self.tab_view = customtkinter.CTkTabview(master=self, fg_color= "#F0F0F0", text_color="white", width=620, height=400)
        self.tab_view.grid(row=1, padx=20, pady=20)

        self.tab_view.add("All")
        self.all_tab = CTkListbox(master=self.tab_view.tab("All"), text_color="black", width=620, height=400)
        self.all_tab.grid(row=0)

        self.tab_view.add("Top-ups")
        self.top_ups_tab = CTkListbox(master=self.tab_view.tab("Top-ups"), text_color="black", width=620, height=400)
        self.top_ups_tab.grid(row=0)

        self.tab_view.add("Exchanges")
        self.exchanges_tab = CTkListbox(master=self.tab_view.tab("Exchanges"),text_color="black", width=620, height=400)
        self.exchanges_tab.grid(row=0)

        self.tab_view.add("Received")
        self.transfers_in_tab = CTkListbox(master=self.tab_view.tab("Received"), text_color="black", width=620, height=400)
        self.transfers_in_tab.grid(row=0)

        self.tab_view.add("Sent")
        self.transfers_out_tab = CTkListbox(master=self.tab_view.tab("Sent"), text_color="black", width=620, height=400)
        self.transfers_out_tab.grid(row=0)

        self.display_transactions()

        home_button = customtkinter.CTkButton(self, text="Home", font=("Helvetica", 18), command=self.launch_home_page, width=180, height=40)
        home_button.grid(row=2, pady=10, padx = 10)

        pdf_button = customtkinter.CTkButton(self, text="Export PDF", font=("Helvetica", 18), command=self.generate_and_send_statement, width=180, height=40)
        pdf_button.grid(row=3, pady=10, padx=10)


    def display_transactions(self):
        sorted_transactions = sorted(self.transactions, key=lambda x: x[10], reverse=True)
        top_ups = sorted([t for t in sorted_transactions if t[1] == "top-up"], key=lambda x: x[10], reverse=True)
        exchanges = sorted([t for t in sorted_transactions if t[1] == "exchange"], key=lambda x: x[10], reverse=True)
        transfers_in = sorted([t for t in sorted_transactions if t[1] == "transfer" and t[3] == self.uid and t[2] != self.uid], key=lambda x: x[10], reverse=True)
        transfers_out = sorted([t for t in sorted_transactions if t[1] == "transfer" and t[2] == self.uid and t[3] != self.uid], key=lambda x: x[10], reverse=True)

        i = 0
        for t in sorted_transactions:
            text_line = self.get_tuple_text(t)
            self.all_tab.insert(i, text_line)
            i = i + 1

        i = 0
        for t in top_ups:
            text_line = self.get_tuple_text(t)
            self.top_ups_tab.insert(i, text_line)
            i = i + 1

        i = 0
        for t in exchanges:
            text_line = self.get_tuple_text(t)
            self.exchanges_tab.insert(i, text_line)
            i = i + 1

        i = 0
        for t in transfers_in:
            text_line = self.get_tuple_text(t)
            self.transfers_in_tab.insert(i, text_line)
            i = i + 1

        i = 0
        for t in transfers_out:
            text_line = self.get_tuple_text(t)
            self.transfers_out_tab.insert(i, text_line)
            i = i + 1


    def get_tuple_text(self, t):
        if t[1] == "top-up":
            line = "Added " + t[6] + " " + t[7] + " via " + t[4] + " - " + t[10] + "\n"
        elif t[1] == "exchange":
            line = "Exchanged " + t[6] + " " + t[7] + " <-> " + t[8] + " " + t[9] + " - " + t[10] + "\n"

        elif t[1] == "transfer" and t[2] == self.uid and t[3] != self.uid:
            line = "Sent " + t[6] + " " + t[7] + " to " + self.db.get_name(t[3]) + " - " + t[10] + "\n"

        elif t[1] == "transfer" and t[3] == self.uid and t[2] != self.uid:
            line = "Received " + str(t[8]) + " " + str(t[9]) + " from " + self.db.get_name(str(t[2])) + " - " + str(t[10]) + "\n"
        else:
            line = "error"
        return line


    def generate_and_send_statement(self):
        user_email = self.db.get_email(self.uid)
   
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Statement", ln=True, align="C")

        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Account holder: {self.db.get_name(self.uid)}", ln=True)
        pdf.cell(200, 10, txt=f"Date of generation: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", size=10)
        
        for tx in self.transactions:
            pdf.cell(200, 8, txt=f"{tx[10]} | {tx[1]} | {tx[8]} {tx[9]}", ln=True)

        pdf_data = pdf.output(dest='S').encode('latin1')
        
        pdf_buffer = io.BytesIO(pdf_data)
         
        send_mail_with_pdf(
            to_address=user_email,
            subject="Statement",
            body="Hello, \nHere you can find the statement in PDF format.",
            pdf_buffer=pdf_buffer
        )


    def launch_home_page(self):
        home_page_frame = home_page.HomePage(self.parent, user=self.user, db=self.db)
        home_page_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        home_page_frame.tkraise()

