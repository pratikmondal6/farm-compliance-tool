import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import time

def draw_buffer(gdf1,gdf2):
# # Step 1: Buffer both datasets by 10 meters
#     buffer1 = gdf1.buffer(20)
#     buffer2 = gdf2.buffer(20)

#     # Step 2: Find the intersection of the two buffered areas
#     proximity_zone = buffer1.unary_union.intersection(buffer2.unary_union)

#     # Optional: Check if the zone exists
#     if not proximity_zone.is_empty:
#         # Step 3: Create a small polygon inside that proximity zone
#         # For simplicity, we use a small buffer around the centroid
#         new_polygon = Point(proximity_zone.centroid.x, proximity_zone.centroid.y).buffer(1)

#         # Step 4: Create a GeoDataFrame for the new polygon
#         gdf_new = gpd.GeoDataFrame(geometry=[new_polygon], crs=gdf1.crs)

#         # Step 5: Plot all
#         fig, ax = plt.subplots(figsize=(8, 8))
#         gdf1.plot(ax=ax, color='skyblue', label='Dataset 1')
#         gdf2.plot(ax=ax, color='orange', edgecolor='black', label='Dataset 2')
#         gpd.GeoSeries(proximity_zone).plot(ax=ax, color='none', edgecolor='red', linestyle='--', label='10m Proximity Zone')
#         gdf_new.plot(ax=ax, color='green', edgecolor='black', label='New Polygon')

#         plt.title("Polygon Within 10m Proximity Zone Between Datasets")
#         # plt.legend()
#         # plt.show()
#         plt.savefig("budderdrawn.png", dpi=300, bbox_inches='tight')
#         plt.close()
#     else:
#         print("No proximity zone found within 10 meters.")
    buffer1 = gdf1.buffer(20)
    buffer2 = gdf2.buffer(20)

    # Step 2: Find the intersection of the buffers (10m proximity zone)
    proximity_zone = buffer1.unary_union.intersection(buffer2.unary_union)

    # Step 3: Clip the proximity zone to Dataset 2's buffer only
    # This restricts the zone to the "side" of Dataset 2
    proximity_on_side_of_gdf2 = proximity_zone.intersection(buffer2.unary_union)

    # Step 4: Create a polygon within the restricted proximity zone
    if not proximity_on_side_of_gdf2.is_empty:
        centroid = proximity_on_side_of_gdf2.centroid
        new_polygon = centroid.buffer(1)  # adjust size as needed
        gdf_new = gpd.GeoDataFrame(geometry=[new_polygon], crs=gdf1.crs)

        # Plot
        fig, ax = plt.subplots(figsize=(8, 8))
        gdf1.plot(ax=ax, color='skyblue', label='Dataset 1')
        gdf2.plot(ax=ax, color='orange', edgecolor='black', label='Dataset 2')
        gpd.GeoSeries(proximity_on_side_of_gdf2).plot(ax=ax, color='none', edgecolor='red', linestyle='--', label='10m Zone (facing Dataset 2)')
        gdf_new.plot(ax=ax, color='green', edgecolor='black', label='New Polygon')
        plt.title("Polygon Within 10m Zone Toward Dataset 2")
        # plt.legend()
        # plt.show()
        plt.savefig("budderdrawn.png", dpi=300, bbox_inches='tight')
        plt.close()
    else:
        print("No proximity zone on the side of Dataset 2.")

def draw_buffer_one_side(gdf1,gdf2,bufferVal):
    # Step 0: Use projected CRS (meters)
    # gdf1 = gdf1.to_crs(epsg=32633)
    # gdf2 = gdf2.to_crs(gdf1.crs)

    line_geom = gdf1.geometry.unary_union
    poly_geom = gdf2.geometry.unary_union

    # Step 1: Create one-sided buffers on both sides of the line
    buffer_left = line_geom.buffer(bufferVal, single_sided=True)
    reversed_line = LineString(list(line_geom.coords)[::-1])
    buffer_right = reversed_line.buffer(bufferVal, single_sided=True)

    # Step 2: Calculate minimum distance from each buffer to the polygon
    min_dist_left = buffer_left.distance(poly_geom)
    min_dist_right = buffer_right.distance(poly_geom)

    # Step 3: Choose side where distance is smaller (and < threshold)
    threshold = 15  # meters
    chosen_buffer = None
    if min_dist_left < min_dist_right and min_dist_left < threshold:
        chosen_buffer = buffer_left
        buffer_side = "left"
    elif min_dist_right < threshold:
        chosen_buffer = buffer_right
        buffer_side = "right"

    # Step 4: Intersect with polygon buffer (optional, to trim area)
    if chosen_buffer:
        poly_buffer = poly_geom.buffer(bufferVal)
        proximity_area = chosen_buffer.intersection(poly_buffer)

        # Step 5: Add new polygon inside the proximity zone
        centroid = proximity_area.centroid
        # new_polygon = centroid.buffer(1)
        # gdf_new = gpd.GeoDataFrame(geometry=[new_polygon], crs=gdf1.crs)

        # Step 6: Plot
        fig, ax = plt.subplots(figsize=(8, 8))
        gdf1.plot(ax=ax, color='skyblue', label='Dataset 1')
        gdf2.plot(ax=ax, color='orange', edgecolor='black', label='Dataset 2')
        gpd.GeoSeries(proximity_area).plot(ax=ax, color='none', edgecolor='red', linestyle='--', label=f'{buffer_side.title()} Side Proximity Zone')
        # gdf_new.plot(ax=ax, color='green', edgecolor='black', label='New Polygon')
        plt.title("Region of field that overlaps with the buffer zone")
        timestamp = int(time.time() * 1000)
        image_path=f"./images/image{timestamp}.png"
        plt.savefig(image_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {"image_path":image_path,"buffer_coordinates":gpd.GeoSeries(proximity_area).geometry.to_json()}
    else:
        print("No buffer side is within the proximity threshold.")
        return {"image_path":"","buffer_coordinates":{}}
