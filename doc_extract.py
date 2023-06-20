import csv
import PyPDF2
import re

class DocumentDataExtraction:

    def extract_invoice_number(text):
        invoice_number_regex = r'Invoice Number\s*:\s*([\w-]+)'
        match = re.search(invoice_number_regex, text)
        return match.group(1) if match else ''

    def extract_invoice_date(text):
        invoice_date_regex = r'Invoice Date\s*:\s*([\d.]+)'
        match = re.search(invoice_date_regex, text)
        return match.group(1) if match else ''

    def extract_order_number(text):
        invoice_number_regex = r'Order Number:\s*([\w-]+)'
        match = re.search(invoice_number_regex, text)
        return match.group(1) if match else ''

    def extract_order_date(text):
        order_date_regex = r'Order Date\s*:\s*([\d.]+)'
        match = re.search(order_date_regex, text)
        return match.group(1) if match else ''


    def extract_billing_address(text):
        billing_address_regex = r'Billing Address\s*:\s*([\w\s,]+)'
        match = re.search(billing_address_regex, text)
        return match.group(1).strip() if match else ''

    def extract_shipping_address(text):
        shipping_address_regex = r'Shipping Address\s*:\s*([\w\s,]+)'
        match = re.search(shipping_address_regex, text)
        return match.group(1).strip() if match else ''

    def extract_invoice_details(text):
        invoice_number_regex = r'Invoice Details\s*:\s*([\w-]+)'
        match = re.search(invoice_number_regex, text)
        return match.group(1) if match else ''

    def extract_amount_in_words(text):
        amount_in_words_regex = r'Amount in Words:\s*(.+)'
        match = re.search(amount_in_words_regex, text)
        return match.group(1) if match else ''

    def extract_sold_by(text):
        sold_by_regex = r'Sold By\s*:\s*([\w\s,-]+)'
        match = re.search(sold_by_regex, text)
        return match.group(1).strip() if match else ''

    def extract_invoice_info(file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            invoice_info = []

            for page_number in range(num_pages):
                page = reader.pages[page_number]
                text_content = page.extract_text()
                invoice_number = DocumentDataExtraction.extract_invoice_number(text_content)
                order_number = DocumentDataExtraction.extract_order_number(text_content)
                order_date = DocumentDataExtraction.extract_order_date(text_content)
                invoice_details = DocumentDataExtraction.extract_invoice_details(text_content)
                invoice_date = DocumentDataExtraction.extract_invoice_date(text_content)
                shipping_address = DocumentDataExtraction.extract_shipping_address(text_content)
                billing_address = DocumentDataExtraction.extract_billing_address(text_content)
                sold_by = DocumentDataExtraction.extract_sold_by(text_content)
                amount_in_words = DocumentDataExtraction.extract_amount_in_words(text_content)


                invoice_info.append({
                    # 'Page': page_number + 1,
                    'Invoice Number': invoice_number,
                    'Invoice Date': invoice_date,
                    'Invoice Details' : invoice_details,
                    'Order Number' : order_number,
                    'Order Date' : order_date,
                    'Shipping Address' : shipping_address,
                    'Billing Address' : billing_address,
                    'Sold By' : sold_by,
                    'Amount' : amount_in_words,
                })

        return invoice_info

    def write_to_csv(file_path, invoice_info_list):
        if not invoice_info_list:
            return

        keys = invoice_info_list[0][0].keys()

        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)

            if file.tell() == 0:  # Check if the file is empty
                writer.writeheader()

            for invoice_info in invoice_info_list:
                writer.writerows(invoice_info)
