from fpdf import FPDF
import os
import time


def generate_regulations_pdf(regulations, output_folder="pdfs", filename=None,water_regulation="",image_path=""):
    os.makedirs(output_folder, exist_ok=True)
    # Use timestamp in milliseconds if filename not given
    item_name=filename
    timestamp = int(time.time() * 1000)
    filename = f"regulations_{filename}_{timestamp}.pdf"

    filepath = os.path.join(output_folder, filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Regulations Report for {item_name}", ln=True, align='C')
    if water_regulation:
        pdf.set_font("Arial", 'I', 11)
        pdf.multi_cell(0, 8, water_regulation)
        
    pdf.ln(10)

    # Add image if path is given
    if image_path and os.path.exists(image_path):
        # x, y = position from top-left corner (in mm)
        # w = width in mm; height is scaled automatically
        pdf.image(image_path, x=10, y=None, w=180)  # You can adjust these values
        pdf.ln(10)  # 
    
    for idx, reg in enumerate(regulations, start=1):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{idx}. {reg['code']} ({reg['category']})", ln=True)
        pdf.set_font("Arial", 'I', 11)
        pdf.multi_cell(0, 8, f"DE: {reg['text_deutsch']}")
        pdf.ln(1)
        pdf.multi_cell(0, 8, f"EN: {reg['text_englisch']}")
        pdf.ln(6)  # space between entries

    pdf.output(filepath)
    print(f"✅ PDF saved to: {filepath}")
    return filepath
