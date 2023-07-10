import PyPDF2
import re
import tabula
import pandas as pd
import numpy as np
from camelot import read_pdf


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    text = ''
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text


def extract_invoice_number(text):
    patterns = ['Invoice No.', 'Order No.', 'Invoice Number', 'Order #']
    for pattern in patterns:
        match = re.search(r'{}(\s*:\s*|\s+)(\w+)'.format(pattern), text, re.IGNORECASE)
        if match:
            return match.group(2)
    return None


def extract_invoice_date(text):
    patterns = ['Invoice Date', 'Date of Issue', 'Billing Date', 'Order Date', 'Date']
    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_total_amount(text):
    patterns = ['Total', 'TOTAL', 'Amount Due', 'Total Payable', 'Grand Total']
    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            line = match.group(2).replace(',', '')
            pattern = r'(\d+\.\d+)'
            match = re.search(pattern, line)
            if match:
                result = match.group(1)
                return result
    return None


def extract_table_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    table_label = [table.columns.tolist() for table in tables]
    table_header = None

    for sublist in table_label:
        lowercase_sublist = [item.lower() for item in sublist]
        if 'item' in lowercase_sublist or 'product' in lowercase_sublist or 'product name' in lowercase_sublist or 'item name' in lowercase_sublist:
            table_header = sublist
            break
    table_data = [table.values.tolist() for table in tables]
    clean_table = []
    for data in table_data[1]:
        if len(data) == len(table_header):
            my_dict = {k: v for k, v in zip(table_header, data)}
            clean_table.append(my_dict)
    return clean_table


def extract_table_using_camelot(pdf_path):
    tables = read_pdf(pdf_path, pages="all", flavor='stream')
    allin = []
    last_table_index = tables.n - 1

    last_table = tables[last_table_index]

    table_data = last_table.df
    table_data = table_data.iloc[3:]

    allin.append(table_data)
    df = pd.concat(allin)
    df = df.reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.reset_index(drop=True)
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
    dict_list = []
    for index, row in df.iterrows():
        dict_list.append(row.to_dict())
    return dict_list


def extract_information_from_invoice(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    invoice_number = extract_invoice_number(extracted_text)
    invoice_date = extract_invoice_date(extracted_text)
    total_amount = extract_total_amount(extracted_text)
    # table = extract_table_using_camelot(pdf_path)
    table = extract_table_from_pdf(pdf_path)
    invoice_info = {
        "invoice_number": str(invoice_number),
        "invoice_date": str(invoice_date),
        "total_amount": str(total_amount),
        "items": table
    }
    return invoice_info


# Example usage
invoice_pdf_path = 'invoices/13.pdf'
invoice_info = extract_information_from_invoice(invoice_pdf_path)
print(invoice_info)
