import streamlit as st
from PIL import Image
import pickle
import numpy as np
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import altair_ally as aly
import altair as alt

import datetime
import ee
import streamlit as st
import geemap.foliumap as geemap

## Set page icon
icon = Image.open("./resources/favicon.ico")

## Set page title and layout
st.set_page_config(
    page_title="Poverty Visualization - Povtrait",
    page_icon=icon,
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.sidebar.title("About")
st.sidebar.info(
    """
    Web App URL: <https://povtrait.streamlit.app/>

    GitHub Repository: <https://github.com/fitriandriastuti/povtrait>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Abd. Hadi Asfarangga: 
    [GitHub](https://github.com/hadi-asfarangga) | | [LinkedIn](https://www.linkedin.com/in/abdul-hadi-asfarangga-76b698130/)

    Baiq Nurul Haqiqi:
    [GitHub](https://github.com/bnhaqiqi) | [Twitter](https://twitter.com/fitriandriast) | [LinkedIn](https://www.linkedin.com/in/baiq-nurul-haqiqi/)

    Ferdian Fadly: <ferdifadly.blogspot.com/>
    [GitHub](https://github.com/ferdi-fadly) | [Twitter](https://twitter.com/ferdianfadly) | [LinkedIn](https://www.linkedin.com/in/ferdian-fadly-81826466/)

    Fitri Andri Astuti: <fitrengineer.com>
    [GitHub](https://github.com/fitriandriastuti) | [Twitter](https://twitter.com/fitriandriast) | [YouTube](https://www.youtube.com/channel/UC1CC_1KKL32tTAFsNNBBlag) | [LinkedIn](https://www.linkedin.com/in/fitriandriastuti)

    Muhammad Syahrul: 
    [GitHub](https://github.com/muhammad92syahrul) | [Twitter](https://twitter.com/pegawaiumbi) | [YouTube](https://www.youtube.com/channel/UCON57Bvk-qsED80SI8jlqkw) | [LinkedIn](https://www.linkedin.com/in/muhammad-syahrul-aa8892218/)

    """
)

# Set title
st.title('Poverty Visualization')

# Load the data
import json
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

data_poverty = pd.read_excel("data/complile_poverty_ntl_viirs_all_country.xlsx", sheet_name="prediction_allcountries")
data_geo = json.load(open('data/countries.geojson'))
years = [str(year) for year in range(2012, 2023)]
year = st.selectbox("Select Year", years)
quarterly = [str(year) for year in range(1, 5)]
option_quarter = st.selectbox("Select Quarter", (quarterly))

def center():
    address = 'Indonesia'
    geolocator = Nominatim(user_agent="id_explorer")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

def threshold(data):
    threshold_scale = np.linspace(data_poverty[year].min(),
                              data_poverty[year].max(),
                              10, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale

def show_maps(data, threshold_scale):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_poverty,
        columns=['Country Code',year],
        key_on='feature.properties.ISO_A3',
        threshold_scale=threshold_scale,
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Poverty Levels",
        highlight=True,
        reset=True).add_to(world_map)

    folium.LayerControl().add_to(world_map)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['ADMIN'],
                                                        aliases=['ADMIN'],
                                                        labels=True))
    folium_static(world_map)

centers = center()

world_map = folium.Map(tiles="OpenStreetMap", location=[centers[0], centers[1]], zoom_start=3)

show_maps(year, threshold(year))

# # Create multiple tabs
# vis_tab, pred_single_tab  = st.tabs(["Map Visualization", ""])
#
# # import leafmap
# # import geopandas as gpd
# # import leafmap.leafmap as leafmap  # for ipyleaflet only
#
# # path_to_data = gpd.datasets.get_path("data/complile_poverty_ntl_viirs_all_country.xlsx")
# # gdf = gpd.read_file(path_to_data, sheet_name="prediction_allcountries")
# # print(gdf)
#
# ###### Tab 1: Visualisation ######
# with vis_tab:
#     col1, col2 = st.columns([4, 1])
#     countries_geojson = 'data/countries.geojson'
#
#     Map = geemap.Map()
#     Map.add_basemap("HYBRID")
#
#     # markdown = """
#     #     - [Dynamic World Land Cover](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1?hl=en)
#     #     - [ESA Global Land Cover](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100)
#     #     - [ESRI Global Land Cover](https://samapriya.github.io/awesome-gee-community-datasets/projects/esrilc2020)
#     #
#     # """
#
#     with col2:
#
#         longitude, latitude, zoom = 117.153709, -0.502106, 5
#         Map.setCenter(longitude, latitude, zoom)
#
#         years = [str(year) for year in range(2012, 2023)]
#         option_years = st.selectbox("Select Year", (years))
#
#         quarterly = [str(year) for year in range(1, 5)]
#         option_quarter = st.selectbox("Select Quarter", (quarterly))
#
#         Map.add_geojson(countries_geojson, layer_name="Boundary All Country")
#         # Map.add_data(df, column="country", cmap='Blues', layer_name="Poverty Prediction")
#         # Map.add_gdf(gdf, layer_name="Boundary All Country", fill_colors=["red", "green", "blue"])
#
#         # with st.expander("Data sources"):
#         #     st.markdown(markdown)
#
#     with col1:
#         Map.to_streamlit(height=750)
#
#
# ###### Tab 2: Single Prediction with All Variables ######
# with pred_single_tab:
#     st.subheader("Predicting Poverty with NTL")
#     col2 = st.columns(2)
#
#     # Sliders for the variables
#     with col2[0]:
#         ntl = st.slider(
#             'NTL',
#             0.0, 1.0, 0.5)
#
#
#     # # Create dataframe for the features
#     # features = {
#     #             'NTL': ntl,
#     #             }
#     # features_df = pd.DataFrame([features])
#     #
#     #
#     # prediction = predict_poverty(features_df)
#     #
#     # # Display the prediction
#     # st.markdown('#### Predicted Poverty: ' + str(round(prediction[0], 2)))
#     # #st.markdown('#### Predicted Poverty: ' + str(30))
#






