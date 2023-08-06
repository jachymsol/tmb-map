from pathlib import Path
from PIL import Image
import json

def get_gps_from_exif(exif):
    gps = exif.get(34853, None)
    if gps is None: return None
    #  {1: 'N', 2: (45.0, 53.0, 23.64), 3: 'E', 4: (6.0, 47.0, 53.09), 5: b'\x00', 6: 1017.5947843530591, 12: 'K', 13: 0.0, 16: 'T', 17: 209.47100840336134, 23: 'T', 24: 209.47100840336134, 31: 6.426194078236438}
    # latitude, longitude, altitude, speed, turn, ???, precision
    latitude_multiplier = 1 if gps[1] == "N" else -1
    latitude = (gps[2][0] + gps[2][1] / 60.0 + gps[2][2] / 3600.0) * latitude_multiplier

    longitude_multiplier = 1 if gps[3] == "E" else -1
    longitude = (gps[4][0] + gps[4][1] / 60.0 + gps[4][2] / 3600.0) * longitude_multiplier

    return [longitude, latitude]

def get_time_from_exif(exif):
    time = exif.get(306, None)
    if time is None: return None
    # '2023:07:22 11:08:55'
    time = time.replace(':', '-', 2)
    return time

def get_geojson(img_path):
    img = Image.open(img_path)
    exif = img._getexif()
    return {
        'type': "Feature",
        'geometry': {
            'type': "Point",
            'coordinates': get_gps_from_exif(exif)
        },
        'properties': {
            'time': get_time_from_exif(exif)
            # 'style': {'color': ""},
            # 'icon': "circle",
            # 'iconstyle': {
            #     'fillColor': "#0000FF",
            #     'fillOpacity': 0.8,
            #     'stroke': 'true',
            #     'radius': 5
            # }
        }
    }

path = Path.cwd() / 'tmb_photos'
imgs = list(path.glob('*.??G'))

geojsons = [get_geojson(img_path) for img_path in imgs]

def filter_fn(geojson):
    if geojson['properties']['time'] is None: return False
    if geojson['geometry']['coordinates'] is None: return False
    if geojson['properties']['time'] < "2023-07-22 00:00:00": return False
    if geojson['properties']['time'] > "2023-07-30 23:59:59": return False
    return True

filtered_geojsons = [geojson for geojson in geojsons if filter_fn(geojson)]
sorted_geojsons = sorted(filtered_geojsons, key=lambda x: x['properties']['time'])
print(len(sorted_geojsons))

with open('tmb_geojson.json', 'w') as f:
    json.dump(sorted_geojsons, f)
