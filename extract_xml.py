import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_iso11783_taskdata(xml_file):
    root = ET.fromstring(xml_file)
    # root = tree.getroot()

    data = {}

    # Root attributes (general info)
    data['VersionMajor'] = root.attrib.get('VersionMajor')
    data['VersionMinor'] = root.attrib.get('VersionMinor')
    data['ManagementSoftwareManufacturer'] = root.attrib.get('ManagementSoftwareManufacturer')
    data['ManagementSoftwareVersion'] = root.attrib.get('ManagementSoftwareVersion')
    data['DataTransferOrigin'] = root.attrib.get('DataTransferOrigin')

    # Helper function to parse attributes of elements into dict
    def attr_dict(elem, keys=None):
        if keys:
            return {k: elem.attrib.get(k, '') for k in keys}
        else:
            return elem.attrib.copy()

    # Client (CTR)
    ctr = root.find('CTR')
    if ctr is not None:
        data['Client'] = attr_dict(ctr)

    # Farm (FRM)
    frm = root.find('FRM')
    if frm is not None:
        data['Farm'] = attr_dict(frm)

    # Crop Type (CPC)
    cpc = root.find('CPC')
    if cpc is not None:
        data['CropType'] = attr_dict(cpc)

    # Products (PDT) - there may be multiple
    data['Products'] = {}
    for pdt in root.findall('PDT'):
        pdt_id = pdt.attrib.get('A')
        data['Products'][pdt_id] = attr_dict(pdt)

    # Prescription Field Data (PFD)
    pfd = root.find('PFD')
    if pfd is not None:
        data['Prescription'] = {
            'Attributes': attr_dict(pfd),
            'Polygons': []
        }
        # Extract polygons (PLN) and their line segments (LSG) with points (PNT)
        for pln in pfd.findall('PLN'):
            polygon = {'ID': pln.attrib.get('A'), 'LineSegments': []}
            for lsg in pln.findall('LSG'):
                line_segment = {'ID': lsg.attrib.get('A'), 'Points': []}
                for pnt in lsg.findall('PNT'):
                    point = {
                        'ID': pnt.attrib.get('A'),
                        'Latitude': pnt.attrib.get('C'),
                        'Longitude': pnt.attrib.get('D'),
                    }
                    line_segment['Points'].append(point)
                polygon['LineSegments'].append(line_segment)
            data['Prescription']['Polygons'].append(polygon)
        # Single points under PFD as well
        points = []
        for pnt in pfd.findall('PNT'):
            points.append({
                'ID': pnt.attrib.get('A'),
                'Latitude': pnt.attrib.get('C'),
                'Longitude': pnt.attrib.get('D'),
            })
        if points:
            data['Prescription']['Points'] = points

    # Variable Product Number (VPN)
    vpn = root.find('VPN')
    if vpn is not None:
        data['VariableProductNumber'] = attr_dict(vpn)

    # Task (TSK)
    tsk = root.find('TSK')
    if tsk is not None:
        data['Task'] = {
            'Attributes': attr_dict(tsk),
            'OTPs': [],
            'Zones': [],
            'Time': None,
            'PAN': None,
            'DLT': None,
            'CAN': False
        }
        # OTP elements
        for otp in tsk.findall('OTP'):
            data['Task']['OTPs'].append(attr_dict(otp))

        # Task Zones (TZN) and PDVs inside them
        for tzn in tsk.findall('TZN'):
            zone = attr_dict(tzn)
            zone['PDVs'] = []
            for pdv in tzn.findall('PDV'):
                zone['PDVs'].append(attr_dict(pdv))
            data['Task']['Zones'].append(zone)

        # Time (TIM)
        tim = tsk.find('TIM')
        if tim is not None:
            data['Task']['Time'] = attr_dict(tim)

        # PAN
        pan = tsk.find('PAN')
        if pan is not None:
            data['Task']['PAN'] = attr_dict(pan)

        # DLT
        dlt = tsk.find('DLT')
        if dlt is not None:
            data['Task']['DLT'] = attr_dict(dlt)

        # CAN element (just presence boolean)
        can = tsk.find('CAN')
        data['Task']['CAN'] = can is not None

    return data
def extract_products_except_first_and_last(products_dict):
    filtered = {}
    for key, attrs in products_dict.items():
        name = attrs.get('B', '').lower()
        if 'unbekannt' not in name and 'gemisch' not in name:
            filtered[key] = attrs
    return filtered
# Example usage:
# if __name__ == "__main__":
#     filename = "./TASKDATA.XML"  # Path to your ISO11783 XML file
#     extracted_info = parse_iso11783_taskdata(filename)
    
#     import pprint
#     pprint.pprint(extracted_info)
