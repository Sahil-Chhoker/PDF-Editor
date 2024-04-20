import tkinter as tk
import os
import shutil
from tkinter import filedialog
from pathlib import Path
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from pdf2image import convert_from_path
from dotenv import load_dotenv 
import groupdocs_conversion_cloud

load_dotenv()
# ?: Using GroupDocs Cloud Service API Here
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

poppler_path = os.getenv('POPPLER_PATH')


def get_file_name(file_path):
    return Path(file_path).stem


def convert_txtfile_to_pdf(file_path, output_path):
    pdf = FPDF()
    pdf.add_page()

    fname = get_file_name(file_path)
    with open(file_path, 'r') as file:
        for text in file:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(w=0, h=10, txt=text, align="L")
        
    pdf.output(f"{output_path}/{fname}.pdf")


def splitting_pdf(file_path, page_no, trim_from_behind):
    fname = get_file_name(file_path)
    pdf = PdfReader(file_path)
    no_of_pages = len(pdf.pages)
    
    pdf_writer = PdfWriter()
    if not trim_from_behind:
        for i in range(page_no):
            pdf_writer.add_page(pdf.pages[i])
    else: 
        for i in range(page_no):
            pdf_writer.add_page(pdf.pages[no_of_pages - page_no + i])
        
    output_filename = f"{fname}_page_{page_no}.pdf"

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

    print(f'Created: {output_filename}')


def merging_pdf(file_paths, output_path):
    pdf_merger = PdfMerger()
    fname = ''

    for file_path in file_paths:
        with open(file_path, 'rb') as pdf:
            pdf_merger.append(pdf)
            fname += get_file_name(file_path) + " + "

    output_filename = f"{output_path}/merged_{fname}.pdf"

    with open(output_filename, 'wb') as out:
        pdf_merger.write(out)

    print(f'Merged: {output_filename}')


def convert_to_image(file_path, output_path):
    fname = get_file_name(file_path)
    images = convert_from_path(file_path, poppler_path=poppler_path)
    for i, image in enumerate(images):
        image.save(f'{output_path}/{fname}_page_{i - 1}.jpg', 'JPEG')

    print(f'Images saved to {output_path}')


def convert_to_ppt(file_path, output_path):
    api = groupdocs_conversion_cloud.ConvertApi.from_keys(client_id, client_secret)

    request = groupdocs_conversion_cloud.ConvertDocumentDirectRequest("pptx", file_path)

    response = api.convert_document_direct(request)
    shutil.move(response, output_path)
    print(f'Converted PowerPoint saved to {output_path}')


def select_file_and_action(action):
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text files, Pdf files", "*.txt *.pdf")])
    if file_path:
        if action == "split":
            page_no = int(entry.get())
            trim_from_behind = trim_var.get()
            splitting_pdf(file_path, page_no, trim_from_behind)
        elif action == "convert_to_image":
            output_path = filedialog.askdirectory(title="Select Output Directory")
            convert_to_image(file_path, output_path)
        elif action == "convert_to_ppt":
            output_path = filedialog.askdirectory(title="Select Output Directory")
            convert_to_ppt(file_path, output_path)


def select_multiple_files(action):
    file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("Text files, Pdf files", "*.txt *.pdf")])
    if file_paths == None or file_paths == []:
        raise ImportError("Files were not imported, try again!")
    
    for file_path in file_paths:
        if action == "convert":
            output_path = filedialog.askdirectory(title="Select Output Directory")
            convert_txtfile_to_pdf(file_path, output_path)

    if action == "merge":
        if len(file_paths) <= 1:
            raise ValueError("Can't merge a single file, select more than one to continue!")
        output_path = filedialog.askdirectory(title="Select Output Directory")
        merging_pdf(file_paths, output_path)


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)

    window.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")


def main():
    root = tk.Tk()
    root.title("PDF Editor")
    root.resizable(False, False)  

    convert_button = tk.Button(root, text="Split PDF", command=lambda: select_file_and_action("split"))
    convert_button.grid(row=0, column=0, pady=10)

    entry_label = tk.Label(root, text="Enter number of pages:")
    entry_label.grid(row=0, column=1, pady=10)

    global entry
    entry = tk.Entry(root)
    entry.grid(row=0, column=2, pady=10)

    global trim_var
    trim_var = tk.BooleanVar()
    trim_checkbox = tk.Checkbutton(root, text="Trim from behind", variable=trim_var)
    trim_checkbox.grid(row=0, column=3, pady=10)

    convert_button = tk.Button(root, text="Convert Text to PDF", command=lambda: select_multiple_files("convert"))
    convert_button.grid(row=1, column=0, pady=10)

    merge_button = tk.Button(root, text="Merge PDFs", command=lambda: select_multiple_files("merge"))
    merge_button.grid(row=1, column=1, pady=10)

    convert_to_img_button = tk.Button(root, text="Convert PDF to Images", command=lambda: select_file_and_action("convert_to_image"))
    convert_to_img_button.grid(row=1, column=2, pady=10)

    convert_to_ppt_button = tk.Button(root, text="Convert PDF to PowerPoint", command=lambda: select_file_and_action("convert_to_ppt"))
    convert_to_ppt_button.grid(row=1, column=3, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
