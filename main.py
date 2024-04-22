import tkinter as tk
import os, random
import img2pdf
import shutil
from tkinter import filedialog, ttk
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

font_family = ["Courier", "Arial", "Times", "Symbol", "ZapfDingbats"]


def get_file_name(file_path):
    return Path(file_path).stem

def random_file_no():
    return random.randint(0, 1000)


def convert_txtfile_to_pdf(file_path, output_path, selected_font):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(selected_font, size=10)
    
    fname = get_file_name(file_path)
    with open(file_path, 'r') as file:
        for text in file:
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
    fname = random_file_no()

    for file_path in file_paths:
        with open(file_path, 'rb') as pdf:
            pdf_merger.append(pdf)

    output_filename = f"{output_path}/merged_file{fname}.pdf"

    with open(output_filename, 'wb') as out:
        pdf_merger.write(out)

    print(f'Merged: {output_filename}')


def convert_to_image(file_path, output_path):
    fname = get_file_name(file_path)
    images = convert_from_path(file_path, poppler_path=poppler_path)
    for i, image in enumerate(images):
        image.save(f'{output_path}/{fname}_page_{i + 1}.jpg', 'JPEG')

    print(f'Images saved to {output_path}')


def convert_to_ppt(file_path, output_path):
    api = groupdocs_conversion_cloud.ConvertApi.from_keys(client_id, client_secret)

    request = groupdocs_conversion_cloud.ConvertDocumentDirectRequest("pptx", file_path)

    response = api.convert_document_direct(request)
    shutil.move(response, output_path)
    print(f'Converted PowerPoint saved to {output_path}')


def convert_img_files_to_pdf(file_paths, output_path):
    image_data = []
    fname = random_file_no()

    for file_path in file_paths:
        with open(file_path, 'rb') as img_file:
            image_data.append(img_file.read())
    
    pdf_data = img2pdf.convert(image_data)

    output_file = f'{output_path}/img_to_pdf{fname}.pdf'
    with open(output_file, "wb") as file:
        file.write(pdf_data)

    print(f'Images converted and saved as PDF to: {output_path}')


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
    file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("Text files, Pdf files, Image files", "*.txt *.pdf *.jpg *.jpeg *.png")])
    if file_paths == None or file_paths == []:
        raise ImportError("Files were not imported, try again!")
    
    if action == "convert":
        for file_path in file_paths:
            selected_font = font_combobox.get()
            output_path = filedialog.askdirectory(title="Select Output Directory")
            convert_txtfile_to_pdf(file_path, output_path, selected_font)
    elif action == "merge":
        if len(file_paths) <= 1:
            raise ValueError("Can't merge a single file, select more than one to continue!")
        output_path = filedialog.askdirectory(title="Select Output Directory")
        merging_pdf(file_paths, output_path)
    elif action == "convert_img_to_pdf":
        output_path = filedialog.askdirectory(title="Select Output Directory")
        convert_img_files_to_pdf(file_paths, output_path)


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

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill='both', expand=True)

    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True)

    # Split PDF tab
    split_frame = tk.Frame(notebook)
    notebook.add(split_frame, text='Split PDF')

    split_label = tk.Label(split_frame, text="Split PDF", font=("Arial", 16, "bold"))
    split_label.pack(pady=10)

    split_button = tk.Button(split_frame, text="Split PDF", command=lambda: select_file_and_action("split"))
    split_button.pack(pady=5)

    entry_label = tk.Label(split_frame, text="Enter no. of pages:")
    entry_label.pack(pady=5)

    global entry
    entry = tk.Entry(split_frame)
    entry.pack(pady=5)

    global trim_var
    trim_var = tk.BooleanVar()

    trim_checkbox = tk.Checkbutton(split_frame, text="Trim from behind", variable=trim_var)
    trim_checkbox.pack(pady=5)

    # Convert Text to PDF tab
    convert_frame = tk.Frame(notebook)
    notebook.add(convert_frame, text='Convert Text to PDF')

    convert_label = tk.Label(convert_frame, text="Convert Text to PDF", font=("Arial", 16, "bold"))
    convert_label.pack(pady=10)

    convert_button = tk.Button(convert_frame, text="Convert Text to PDF", command=lambda: select_multiple_files("convert"))
    convert_button.pack(pady=5)

    text_style_label = tk.Label(convert_frame, text="Text Style:")
    text_style_label.pack(pady=5)

    global font_combobox
    font_combobox = ttk.Combobox(convert_frame, values=font_family, state="readonly")
    font_combobox.current(0)
    font_combobox.pack(pady=5)

    merge_frame = tk.Frame(notebook)
    notebook.add(merge_frame, text='Merge PDFs')

    merge_label = tk.Label(merge_frame, text="Merge PDFs", font=("Arial", 16, "bold"))
    merge_label.pack(pady=10)

    merge_button = tk.Button(merge_frame, text="Merge PDFs", command=lambda: select_multiple_files("merge"))
    merge_button.pack(pady=10)

    # Other Formats tab
    other_formats_frame = tk.Frame(notebook)
    notebook.add(other_formats_frame, text='Convert PDF to Other Formats')

    convert_to_img_button = tk.Button(other_formats_frame, text="Convert PDF to Images", command=lambda: select_file_and_action("convert_to_image"))
    convert_to_img_button.pack(pady=5)

    convert_to_ppt_button = tk.Button(other_formats_frame, text="Convert PDF to PPT", command=lambda: select_file_and_action("convert_to_ppt"))
    convert_to_ppt_button.pack(pady=5)

    convert_img_to_pdf_button = tk.Button(other_formats_frame, text="Convert Images to PDF", command=lambda: select_multiple_files("convert_img_to_pdf"))
    convert_img_to_pdf_button.pack(pady=5)

    # Status bar
    status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    center_window(root, 600, 600)
    root.mainloop()


if __name__ == "__main__":
    main()
