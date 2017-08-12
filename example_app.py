import os

import dotenv
import pandas as pd
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

dotenv.load_dotenv(dotenv.find_dotenv())
key = os.environ.get('GOOGLE_API_KEY')
app = Flask(__name__, template_folder=".")
GoogleMaps(app, key=key)

# import geopandas as gpd
# shape_file = r'..\Data\Pavement Projects 2017\Pavement2017.geojson'
# gdf = gpd.GeoDataFrame.from_file(shape_file)

data = pd.read_csv('merged_data.csv')
icon_link_template = 'http://maps.google.com/mapfiles/ms/icons/{icon_color}-dot.png'

icon_color_map = {
    'pavement': 'blue',
    'ramps': 'green',
    'residential_reconstruction': 'yellow',
    'sidewalks': 'red'
}


def parse_data(series):
    work = series.infrastructure_type
    icon_color = icon_color_map[work]
    icon = icon_link_template.format(icon_color=icon_color)
    infobox = '%s construction' % work

    d = {'icon': icon,
         'lat': series.latitude,
         'lng': series.longitude,
         'infobox': infobox}

    return d

markers = [parse_data(row) for row in data.itertuples()]


@app.route("/")
def mapview():
    # creating a map in the view
    sndmap = Map(
        identifier="sndmap",
        lat=40.717592,
        lng=-89.603804,
        markers=markers

    )
    return render_template('construction_map.html', sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True)
