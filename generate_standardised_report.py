from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import io
from datetime import datetime
import os

templates = Environment(loader=FileSystemLoader("templates"))

def generate_and_save_pdf(products,time,quantity):
    # 1. Render HTML from template
    template = templates.get_template("report.html")
    items = []
    for product in products.keys():
        items.append(products[product]['B'])
    data = {'products':items,"date":time, "quantity":quantity}
    html_out = template.render(**data)

    # 2. Create PDF from rendered HTML
    pdf = HTML(string=html_out).write_pdf()

    # 3. Save PDF to disk (e.g., to /tmp or another location)
    output_dir = "pdfs"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "wb") as f:
        f.write(pdf)

    # 4. Optionally return it as response
    return {
        "message": "PDF generated and saved",
        "filename": filename,
        "path": file_path
    }