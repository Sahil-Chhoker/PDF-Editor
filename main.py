from pathlib import Path
from fpdf import FPDF

def convert_file(file):
    pdf = FPDF()
    pdf.add_page()

    for text in file:
        if len(text) <= 20:
            pdf.set_font("Arial", "B", size=18)
            pdf.cell(w=200, h=10, txt=text, ln=1, align="C")
        else:
            pdf.set_font("Arial", size=15)
            pdf.multi_cell(w=0, h=10, txt=text,align="L")
    pdf.output("result.pdf")

if __name__ == "__main__":
    text_file = Path("C:/MASTER FOLDER/GitHub/PDF-Editor/test/BIODIVERSITY.txt")
    with open(text_file, 'r') as file:
        convert_file(file)