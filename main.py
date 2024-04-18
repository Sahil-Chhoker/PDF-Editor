import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from fpdf import FPDF

def convert_file(file_path):
    pdf = FPDF()
    pdf.add_page()

    name = ''
    with open(file_path, 'r') as file:
        name = file.name
        for text in file:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(w=0, h=10, txt=text, align="L")
        
    pdf.output(f"result.pdf")
    print(name)
            

def select_file():
    file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text files", "*.txt")])
    if file_path:
        convert_file(file_path)

def main():
    root = tk.Tk()
    root.title("Text to PDF Converter")

    button = tk.Button(root, text="Select Text File", command=select_file)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
