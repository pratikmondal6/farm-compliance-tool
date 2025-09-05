import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from pyproj import Transformer
from shapely.ops import transform
from plot_polygons import plot_polygons,plot_two_geodataframes
from draw_buffer import draw_buffer,draw_buffer_one_side
# Load the shapefile


# # If it's a simple Polygon:
# if geom.geom_type == 'Polygon':
#     coords = list(geom.exterior.coords)
#     print("Polygon coordinates:")
#     for coord in coords:
#         print(coord)


# poly = gdf.iloc[0].geometry

# x, y = poly.exterior.xy

# plt.figure()
# plt.plot(x, y, color='blue')
# plt.scatter(x, y, color='red')  # Add red dots for each vertex

# # Annotate with coordinates
# for i, (x_coord, y_coord) in enumerate(zip(x, y)):
#     plt.text(x_coord, y_coord, f'({x_coord:.2f}, {y_coord:.2f})', fontsize=8)

# plt.title("Polygon with Coordinates")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.axis("equal")
# # plt.show()
# plt.savefig("polygon_plot.png")
# print("Plot saved as polygon_plot.png")




# poly1 = [(0,0), (2,0), (2,2), (0,2)]
# poly2 = [(1,1), (3,1), (3,3), (1,3)]
# poly3 = [(3,3), (4,3), (4,4), (3,4)]
# polygons_overlap(poly1, poly2)

# def polygons_overlap(poly1, poly2):
#     # poly1 = Polygon(poly1_coords)
#     # poly2 = Polygon(poly2_coords)

#     return poly1.intersects(poly2).any()

# def check_water_overlap(field_coordinates):
#     gdf = gpd.read_file("./geodata/Gewaesserlinien_GebietNeumuehle.shp")

#     # View the data
#     print(gdf.head())
#     print(gdf.columns)

#     # Print the first row (as a Series with all details)
#     print(len(gdf))
#     poly1 = Polygon(field_coordinates)
#     print(poly1)

# # Wrap in GeoDataFrame, set CRS
#     custom_gdf = gpd.GeoDataFrame(geometry=[poly1], crs="EPSG:4326")

# # Reproject to match original gdf
#     custom_gdf = custom_gdf.to_crs(gdf.crs)
#     print(custom_gdf.geometry)
#     for idx, row in gdf.iterrows():
#         geometry = row.geometry
#         if polygons_overlap(custom_gdf.geometry,geometry):
#             return True
#     return False
        # print(f"Index {idx} → Geometry: {geometry}")


    # Get the first row's geometry
    # geom = gdf.iloc[0].geometry
    
# gdf = gpd.read_file("./geodata/WHGGewAbstand_Polygone.shp")

#     # View the data
# print(gdf.head())
# print(gdf.columns)

#     # Print the first row (as a Series with all details)
# print(gdf.iloc[0])

# Define transformer: WGS84 to ETRS89 / UTM Zone 32N
transformer = Transformer.from_crs("EPSG:4326", "EPSG:25832", always_xy=True)



def polygons_overlap(poly1, poly2,constraint):
    # return poly1.intersects(poly2)  # Both are shapely geometries now
    return poly1.distance(poly2) <= int(constraint)
def check_water_overlap(field_coordinates,constraint):
    # Load waterbody shapefile
    gdf = gpd.read_file("./geodata/Gewaesserlinien_GebietNeumuehle.shp")

    print("GeoDataFrame loaded:")
    print(gdf.head())
    print("Columns:", gdf.columns)
    print("Number of rows:", len(gdf))



    print(gdf.iloc[0].geometry)

    # print(field_coordinates)
    # Input polygon is in EPSG:4326
    input_poly = Polygon(field_coordinates)
    # projected_polygon = transform(transformer.transform, input_poly)
    # print(input_poly)
    # print(projected_polygon)
    gdf_proj = gpd.GeoDataFrame(geometry=[input_poly], crs="EPSG:4326")  # Source CRS
    # plot_two_geodataframes(gdf_proj)

    
    # Target CRS (e.g. ETRS89 / UTM zone 32N)
    target_crs = "EPSG:25832"

    # Reproject polygon to target CRS
    gdf_proj = gdf_proj.to_crs(target_crs)
    print(gdf_proj.iloc[0].geometry)
    overlapped_coordinates=[]
    for idx, row in gdf.iterrows():
        geometry = row.geometry

        if polygons_overlap(gdf_proj.iloc[0].geometry, geometry,constraint):
            print(f"Overlap found with feature index {idx}")
            # print(geometry)
            overlapped_coordinates.append(geometry)
            # return True

    # print("No overlap found.")
    # overlapped_coordinates.append(gdf_proj.iloc[0].geometry)
    gdf2 = gpd.GeoDataFrame(geometry=overlapped_coordinates)
    gdf3 = gpd.GeoDataFrame(geometry=[gdf_proj.iloc[0].geometry])

    # plot_polygons(overlapped_coordinates)
    # plot_two_geodataframes(gdf2,gdf3)
    # draw_buffer(gdf2,gdf3)
    image_path_response =  {"image_path":"","buffer_coordinates":{}}
    if len(overlapped_coordinates) > 0:
        image_path_response = draw_buffer_one_side(gdf2,gdf3,constraint)
        buffer_coordinates = image_path_response["buffer_coordinates"] 
        image_path_response["buffer_coordinates"] = {'field':gdf3.geometry.to_json(), 'water_body':gdf2.geometry.to_json(), 'buffer':buffer_coordinates}
    return {"isOverlap" : len(overlapped_coordinates) > 0, "buffer_path":image_path_response}