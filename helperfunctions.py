import json
def generateBaseMap(default_location, default_zoom_start=12):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

def get_coordinates(city):

    if city == "New York":
        bottomLeft = (40.69849, -74.02729) 
        bottomRight = (40.69849, -73.94225) 
        topLeft = (40.86399,-74.02729) 
        topRight = (40.86399, -73.94225) 
 
    elif city == "London":
        bottomLeft = (51.46705,-0.20001)  
        bottomRight = (51.46705, -0.02912) 
        topLeft = (51.55837,-0.20001) 
        topRight = (51.55837,-0.02912) 

    return bottomLeft, bottomRight, topLeft, topRight

def get_geojson_grid(city, n=10):
    """Returns a grid of geojson rectangles, and computes the exposure in each section of the grid based on the vessel data.

    Parameters
    ----------
    upper_right: array_like
        The upper right hand corner of "grid of grids" (the default is the upper right hand [lat, lon] of the USA).

    lower_left: array_like
        The lower left hand corner of "grid of grids"  (the default is the lower left hand [lat, lon] of the USA).

    n: integer
        The number of rows/columns in the (n,n) grid.

    Returns
    -------

    list
        List of "geojson style" dictionary objects   
    """

    lower_left, lower_right, upper_left, upper_right = get_coordinates(city)  
    all_boxes = []

    lat_steps,lat_stride = np.linspace(lower_left[0], upper_right[0], n, retstep=True)
    lon_steps, lon_stride = np.linspace(lower_left[1], upper_right[1], n, retstep=True)
    
    lower_left = (lower_left[0]-lat_stride,lower_left[1]-lon_stride)
    upper_right = (upper_right[0]+lat_stride,upper_right[1]+lon_stride)
    
    lat_steps,lat_stride = np.linspace(lower_left[0], upper_right[0], n+2, retstep=True)
    lon_steps, lon_stride = np.linspace(lower_left[1], upper_right[1], n+2, retstep=True)

    
    for lat in lat_steps[:-1]:
        for lon in lon_steps[:-1]:
            
            # Define dimensions of box in grid
            upper_left = [lon, lat + lat_stride]
            upper_right = [lon + lon_stride, lat + lat_stride]
            lower_right = [lon + lon_stride, lat]
            lower_left = [lon, lat]

            # Define json coordinates for polygon
            coordinates = [
                upper_left,
                upper_right,
                lower_right,
                lower_left,
                upper_left
            ]

            geo_json = {"type": "FeatureCollection",
                        "properties":{
                            "lower_left": lower_left,
                            "upper_right": upper_right
                        },
                        "features":[]}

            grid_feature = {
                "type":"Feature",
                "geometry":{
                    "type":"Polygon",
                    "coordinates": [coordinates],
                }
            }

            geo_json["features"].append(grid_feature)

            all_boxes.append(geo_json)

    return all_boxes

def draw_grid(grid, default_location):
    m = generateBaseMap(default_location)

    # Add GeoJson to map
    for i, box in enumerate(grid):
        geo_json = json.dumps(box)

        #color = plt.cm.Greens(regional_counts[i] / worst_region)
        color = mpl.colors.to_hex("white")
        gj = folium.GeoJson(geo_json, style_function=lambda feature, 
        color=color: {'color':"grey", 'dashArray': '1, 1', 'fillOpacity': 0.1,})

        #gj.add_child(popups[i])
        m.add_child(gj)
    return m