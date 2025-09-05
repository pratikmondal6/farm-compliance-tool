import httpx
from query_postgres import get_regulations_associated_with_article,get_constraints_associated_with_article
from generate_pdf import generate_regulations_pdf
from field_check import check_water_overlap

async def get_product_codes(chem_products):
    responses=[]
    for products in chem_products.keys():

        url = "https://psm-api.bvl.bund.de/ords/psm/api-v1/mittel/?q=%7B%22MITTELNAME%22%3A%7B%22%24instr%22%3A%22"+chem_products[products]['B']+"%22%7D%7D"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            responses.append({"data":res.json(), "name" : chem_products[products]['B']})
    return responses

async def get_regulations(responses):
    regulations=[]
    for response in responses:
            items = response["data"]["items"]
            name = response["name"]
            code = ""
            for item in items:
                if item['mittelname'] == name:
                    code = item["kennr"]
            url = "https://psm-api.bvl.bund.de/ords/psm/api-v1/auflagen/?q=%7B%22ebene%22%3A%7B%22%24instr%22%3A%22"+code+"%22%7D%7D"
            async with httpx.AsyncClient() as client:
                res = await client.get(url)
                regulations.append({"data":res.json(),"name":name})
    
    return regulations

def get_filtered_regulations(regulations,filter,field_coordinates,standard_report_details):
    final_regulations=[]
    for regulation in regulations:
            # codes = [i["auflage"] for i in regulation["data"]["items"] ]
        codes = [
                i["auflage"]
                for i in regulation["data"]["items"]
                if i["auflage"].startswith(filter)
            ]
        queried_regulation = {"regulations":get_regulations_associated_with_article(codes),"code":regulation["name"]}
        constraints = get_constraints_associated_with_article(codes)
        queried_regulation["water_regulation"]=""
        queried_regulation["water_overlap_found"] = False
        water_overlap_result={"isOverlap":False,"buffer_path":{"imagePath":""}}
        for constraint in constraints:
            if constraint["water"]:
                queried_regulation["water_regulation"] = f"There is an overlap on your field with a water body. Your field should need to keep a {constraint["boundary"]}m buffer zone from river or other type of water bodies "
                water_overlap_result = check_water_overlap(field_coordinates,constraint["boundary"])
                # print(water_overlap_result)
                queried_regulation["water_overlap_found"] = water_overlap_result["isOverlap"]

        print(queried_regulation["water_overlap_found"])
        pdf_path = generate_regulations_pdf(queried_regulation['regulations'],filename=regulation["name"],water_regulation= queried_regulation["water_regulation"] if queried_regulation["water_overlap_found"] else "",image_path = water_overlap_result["buffer_path"]["image_path"])
        queried_regulation["pdf_path"]=pdf_path
        if queried_regulation["water_overlap_found"]:
            queried_regulation["coordinates"] = water_overlap_result['buffer_path']["buffer_coordinates"]
        queried_regulation["standard_report"] = standard_report_details
        final_regulations.append(queried_regulation)
    return final_regulations

def get_field_coordinates(data):
    coordinates = []

    for polygon in data['Prescription'].get('Polygons', []):
        for segment in polygon.get('LineSegments', []):
            for point in segment.get('Points', []):
                lat = float(point['Latitude'])
                lon = float(point['Longitude'])
                coordinates.append((lon, lat))
    coordinates = list(coordinates)
    return coordinates