import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import geopandas as gpd

def plot_polygons(polygon_list, colors=None, edge_color='black', filename='output.png'):
    """
    Plots a list of polygons and saves the figure to a PNG file.

    Args:
        polygon_list (list of list of tuples): Each polygon is a list of (x, y) tuples.
        colors (list of str or None): Fill colors for each polygon. Optional.
        edge_color (str): Color for the edges of the polygons.
        filename (str): Name of the PNG file to save the figure.
    """
    fig, ax = plt.subplots()
    patches = []

    for coords in polygon_list:
        polygon = Polygon(coords, closed=True, edgecolor=edge_color)
        patches.append(polygon)

    p = PatchCollection(patches, facecolors=colors if colors else 'skyblue',
                        edgecolors=edge_color, linewidths=1, alpha=0.6)
    ax.add_collection(p)

    # Set limits based on polygons
    all_x = [x for poly in polygon_list for x, _ in poly]
    all_y = [y for poly in polygon_list for _, y in poly]
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
    ax.set_aspect('equal', 'box')

    plt.title("Polygon Plot")
    plt.grid(True)

    # Save to PNG file
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot saved to '{filename}'")

# # Example usage
# polygons = [
#     [(1, 1), (4, 1), (4, 4), (1, 4)],                 # Square
#     [(5, 2), (6, 4), (7, 3), (6.5, 1.5)],             # Irregular quad
#     [(8, 1), (9, 3), (10, 1)]                         # Triangle
# ]

# colors = ['red', 'green', 'blue']

# plot_polygons(polygons, colors, filename='polygons.png')

def plot_two_geodataframes(gdf1, gdf2, filename='combined_plot.png',
                           color1='skyblue', color2='orange',
                           edge_color='black'):
    """
    Plots two GeoDataFrames on the same matplotlib axis and saves to a PNG.

    Args:
        gdf1, gdf2 (GeoDataFrame): GeoDataFrames containing Polygon or MultiPolygon geometries.
        filename (str): Output PNG filename.
        color1, color2 (str): Fill colors for each GeoDataFrame.
        edge_color (str): Color for polygon edges.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    gdf1.plot(ax=ax, color=color1, edgecolor=edge_color, label='Dataset 1')
    gdf2.plot(ax=ax, color=color2, edgecolor=edge_color, label='Dataset 2')

    ax.set_title("Two GeoDataFrames Overlaid")
    ax.set_aspect('equal')
    plt.axis('off')  # Remove axis for cleaner output

    # Optional: add legend manually
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color1, edgecolor=edge_color, label='Dataset 1'),
        Patch(facecolor=color2, edgecolor=edge_color, label='Dataset 2')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    # Save to file
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Combined plot saved to '{filename}'")