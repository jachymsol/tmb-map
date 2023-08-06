import folium
from folium import plugins

m = folium.Map(
    location=[45.918291, 6.86615],
    zoom_start=15,
    tiles="http://api.mapy.cz/v1/maptiles/outdoor/256/{z}/{x}/{y}?apiKey=GSOZaBVvlUs9mWgGrfcxKbvc2CNT4iyU_AhLOYFLWJ8",
    attr='<img  width="100px" src="https://api.mapy.cz/img/api/logo.svg" >'
)

with open('tmb_geojson.json', 'r') as file:
    plugins.TimestampedGeoJson(
        data=file,
        period="PT1M",
        date_options="YYYY-MM-DD HH:mm:ss"
    ).add_to(m)

m.save('index.html')