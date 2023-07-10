import pdfplumber

def read_pdf(file_path):
    # Open the PDF file in binary mode
    with pdfplumber.open(file_path) as pdf:
        text_content = ""

        # Iterate over each page and extract the text
        for page in pdf.pages:
            text = page.extract_text()
            text_content += text
    return text_content

# # Usage
# text = read_pdf('invoices/4.pdf')
# print(text)