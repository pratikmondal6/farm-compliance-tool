# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from lxml import etree
from extract_xml import parse_iso11783_taskdata,extract_products_except_first_and_last
import httpx
from query_postgres import get_regulations_associated_with_article
from generate_pdf import generate_regulations_pdf
from fastapi.staticfiles import StaticFiles
from utils import get_product_codes,get_regulations,get_filtered_regulations,get_field_coordinates
from field_check import check_water_overlap
from generate_standardised_report  import generate_and_save_pdf

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload-xml/")
async def upload_xml(file: UploadFile = File(...),filter: str=""):
    # Check file type
    if not file.filename.endswith(".XML"):
        raise HTTPException(status_code=400, detail="File must be an XML")

    contents = await file.read()
    try:
        xml_root = parse_iso11783_taskdata(contents)
        chem_products = extract_products_except_first_and_last(xml_root['Products'])
        responses= await get_product_codes(chem_products)
        regulations=await get_regulations(responses)
        standardised_regulation_report = generate_and_save_pdf(chem_products,xml_root['Task']["Time"]["A"],xml_root["VariableProductNumber"]["D"])
        field_coordinates = get_field_coordinates(xml_root)
        final_regulations = get_filtered_regulations(regulations,filter,field_coordinates,standardised_regulation_report)
    except etree.XMLSyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Invalid XML: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Request error: {e}")

    return final_regulations


app.mount("/pdfs", StaticFiles(directory="pdfs"), name="static")