import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

def get_file_name(file_path):
    return Path(file_path).stem

def convert_file(file_path):
    pdf = FPDF()
    pdf.add_page()

    fname = ''
    with open(file_path, 'r') as file:
        fname = get_file_name(file.name)
        for text in file:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(w=0, h=10, txt=text, align="L")
        
    pdf.output(f"{fname}.pdf")

def splitting_pdf(file_path, page_no):
    fname = get_file_name(file_path)
    pdf = PdfReader(file_path)
    
    pdf_writer = PdfWriter()
    if page_no == 1:
        pdf_writer.add_page(pdf.pages[page_no - 1])
    else:
        for i in range(1, page_no + 1):
            pdf_writer.add_page(pdf.pages[i - 1])
        
    output_filename = f"{fname}_page_{page_no}.pdf"

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

    print('Created: {}'.format(output_filename))

def select_file():
    file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text files, Pdf files", "*.txt, *.pdf")])
    if file_path:
        splitting_pdf(file_path, 3)

def main():
    root = tk.Tk()
    root.title("Text to PDF Converter")

    button = tk.Button(root, text="Select Text File", command=select_file)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
