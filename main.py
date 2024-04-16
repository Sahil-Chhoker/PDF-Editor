from pypdf import PdfReader
from pathlib import Path

pdf_path = (Path.home()/ 'C:\MASTER FOLDER\GitHub\PDF-Editor\sample.pdf')

pdf_reader = PdfReader(pdf_path)

for page in pdf_reader.pages:
    print(page.extract_text())
