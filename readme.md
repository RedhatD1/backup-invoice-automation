# Invoice Extraction Module
Takes a PDF as an input and returns a form with the extracted data.

### Usage
Put invoices in "/invoices/" directory

### Setup
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
uvicorn fast_api:app --reload
You need to have java runtime installed

### Installing new libraries
pip3 install <library_name>

### Updating requirements.txt
pip3 freeze > requirements.txt