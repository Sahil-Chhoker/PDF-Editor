import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

def get_file_name(file_path):
    return Path(file_path).stem

def convert_file(file_path):
    pdf = FPDF()
    pdf.add_page()

    fname = get_file_name(file_path)
    with open(file_path, 'r') as file:
        for text in file:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(w=0, h=10, txt=text, align="L")
        
    pdf.output(f"{fname}.pdf")

def splitting_pdf(file_path, page_no):
    fname = get_file_name(file_path)
    pdf = PdfReader(file_path)
    
    pdf_writer = PdfWriter()
    for i in range(page_no):
        pdf_writer.add_page(pdf.pages[i])
        
    output_filename = f"{fname}_page_{page_no}.pdf"

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

    print(f'Created: {output_filename}')

def merging_pdf(file_paths):
    pdf_merger = PdfMerger()
    fname = ''

    for i, file_path in enumerate(file_paths):
        with open(file_path, 'rb') as pdf:
            pdf_merger.append(pdf)
            fname += get_file_name(file_path) + " + "

    output_filename = f"merged_{fname}.pdf"

    with open(output_filename, 'wb') as out:
        pdf_merger.write(out)

    print(f'Merged: {output_filename}')

def select_file_and_action(action):
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text files, Pdf files", "*.txt *.pdf")])
    if file_path:
        if action == "split":
            page_no = int(entry.get())
            splitting_pdf(file_path, page_no)

def select_multiple_files(action):
    file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("Text files, Pdf files", "*.txt *.pdf")])
    if file_paths == None or file_paths == []:
        raise ImportError("Files were not imported, try again!")
    
    for file_path in file_paths:
        if action == "convert":
            convert_file(file_path)

    if action == "merge":
        if len(file_paths) <= 1:
            raise ValueError("Can't merge a single file, select more than one to continue!")
        merging_pdf(file_paths)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)

    window.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")

def main():
    root = tk.Tk()
    root.title("File Converter")
    root.resizable(False, False)  

    center_window(root, 300, 300)

    convert_button = tk.Button(root, text="Convert Text to PDF", command=lambda: select_multiple_files("convert"))
    convert_button.pack(pady=10)

    split_button = tk.Button(root, text="Split PDF", command=lambda: select_file_and_action("split"))
    split_button.pack(pady=10)

    merge_button = tk.Button(root, text="Merge PDFs", command=lambda: select_multiple_files("merge"))
    merge_button.pack(pady=10)

    global entry
    entry_label = tk.Label(root, text="Enter number of pages:")
    entry_label.pack()
    entry = tk.Entry(root)
    entry.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
