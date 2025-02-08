import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP


CURRENCIES = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN',
              'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BOV',
              'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF',
              'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK',
              'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL',
              'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
              'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY',
              'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK',
              'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA',
              'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR',
              'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN',
              'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF',
              'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD',
              'SSP', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP',
              'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF',
              'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW',
              'ZWL']


BANKY_EMAIL_ADDRESS = 'banky.noreply@gmail.com'

AMOUNT_REGEX_PATTERN = "^[0-9]+(?:(?:,|\.)[0-9]*)?$" # type: ignore


def send_mail(to_address, subject, body):
    password = open("mail_pass.txt", "r").read()

    message = MIMEMultipart() 
    message["From"] = BANKY_EMAIL_ADDRESS
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain")) 

    with SMTP("smtp.gmail.com", 587) as server:
        server.starttls() 
        server.login(BANKY_EMAIL_ADDRESS, password)
        server.sendmail(BANKY_EMAIL_ADDRESS, to_address, message.as_string()) 


def send_mail_with_pdf(to_address, subject, body, pdf_buffer):
    password = open("mail_pass.txt", "r").read()

    message = MIMEMultipart()
    message["From"] = BANKY_EMAIL_ADDRESS
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
    pdf_attachment.add_header("Content-Disposition", "attachment", filename="Statement.pdf")
    message.attach(pdf_attachment)

    with SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(BANKY_EMAIL_ADDRESS, password)
        server.sendmail(BANKY_EMAIL_ADDRESS, to_address, message.as_string())


def exchange(from_currency, to_currency, amount):
    if amount == '':
        return ''

    params = {
        'from': from_currency,
        'to': to_currency,
        'amount': amount
    }

    response = requests.get(f'https://api.currencybeacon.com/v1/convert?api_key=dU989ojtVmeKfKFfqJzC2jUntiIBEaoS', params=params)
    data = response.json()
    return round(data['response']['value'], 2)

