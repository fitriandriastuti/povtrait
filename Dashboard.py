import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
import datetime
import calendar
import altair as alt
from geopy.geocoders import Nominatim
import requests
import folium
from streamlit_folium import folium_static
import json


icon = Image.open("./resources/favicon.ico")

st.set_page_config(
    page_title="Dashboard - Povtrait",
    page_icon=icon,
    layout="wide",
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

st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #FFA500;
    margin: auto;
    border-radius: 5px;
    padding: 20px;
}
label[data-testid="stMetricLabel"] > div {
    font-size: 100%;
    justify-content: center;
}
div[data-testid="stMetricValue"] > div {
    font-size: 125%;
    justify-content: center;
}

</style>
""", unsafe_allow_html=True)

#### MAIN ####
image = Image.open('resources/logo-povtrait.png')
st.image(image, width=600)

st.title("TRACKING AND MODELING QUARTERLY POVERTY")
st.markdown(
    """
    Interactive web app to tracking and modeling quarterly poverty with analysis of Nighttime Light satellite imagery data.
    
    
    
    """
)

today = datetime.datetime.now()

price_data = pd.read_excel("data/Gas and Food Price.xlsx")
data_geo = json.load(open('data/countries.geojson'))
data_food_insecurity = pd.read_excel('data/food insecurity.xlsx')
data_poverty = pd.read_excel('data/data kemiskinan.xlsx')
data_poverty_map = pd.read_excel("data/complile_poverty_ntl_viirs_all_country.xlsx", sheet_name="prediction_allcountries")
data_ntl_viirs = pd.read_excel('data/complile_ntl_viirs_all_country.xlsx',sheet_name='yearly')
data_price = pd.read_excel('data/All Prices Data.xlsx', sheet_name='Monthly Indices')

st.markdown("📆 %s, %s %s, %s" % (calendar.day_name[today.weekday()], today.strftime("%b"), today.day, today.year))
metric_col = st.columns(3)

with metric_col[0]:
    st.metric('Avg Poverty', data_poverty.iloc[:,-1:].mean())
    st.metric('Avg Energy Price', round(data_price.loc[:, 'Energy'].to_list()[0], 2))
with metric_col[1]:
    st.metric('Avg Food Insecurity Prevalence', round(data_food_insecurity.iloc[:, -1:].mean(), 2))
    st.metric('Avg Food Price', round(data_price.loc[:, 'Agriculture'].to_list()[0], 2))
with metric_col[2]:
    st.metric('Avg Radiance',round(data_ntl_viirs.loc[data_ntl_viirs["year"] == data_ntl_viirs["year"].max(), 'avg_sol'].mean(), 2))
    st.metric('Avg Food Price', round(data_price.loc[:, 'Fertilizers'].to_list()[0], 2))


#

## Poverty Map ##
st.subheader("Poverty Map")
col1 = st.columns(2)
with col1[0]:
    years = [str(year) for year in range(2012, 2023)]
    year = st.selectbox("Select Year", years)
    quarterly = [str(year) for year in range(1, 5)]
    option_quarter = st.selectbox("Select Quarter", (quarterly))
    data_poverty_map = data_poverty_map[data_poverty_map["year"]==int(year)]
    data_poverty_map = data_poverty_map[data_poverty_map["quarter"]==int(option_quarter)]


def center():
    address = 'Indonesia'
    geolocator = Nominatim(user_agent="id_explorer")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

def threshold(data):
    threshold_scale = np.linspace(data_poverty_map['Poverty'].min(),
                              data_poverty_map['Poverty'].max(),
                              10, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale


def show_maps(data, threshold_scale):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_poverty_map,
        columns=['country_iso3','Poverty'],
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


#for idx in range(len(data_geo['features'])):
#    country_code = data_geo['features'][idx]['properties']['ISO_A3']
#    data_geo['features'][idx]['properties']['Food Insecurity'][year] = data_food_insecurity.loc[data_food_insecurity['Country Code']==country_code,str(year)].tolist()[0]

show_maps(year, threshold(year))