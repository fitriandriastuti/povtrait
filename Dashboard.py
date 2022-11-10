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
    GitHub repository: <https://github.com/fitriandriastuti/povtrait>
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
    background-color: #0094d9;
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

st.title('Poverty Potrait Dashboard')
today = datetime.datetime.now()

price_data = pd.read_excel("data/Gas and Food Price.xlsx")
#df.rename(columns={'Date(Monthly)': 'Date'}, inplace=True)

st.markdown("📆 %s, %s %s, %s" % (calendar.day_name[today.weekday()], today.strftime("%b"), today.day, today.year))
metric_col = st.columns(3)

# with metric_col[0]:
#     st.metric('Latest Anoda', df[df["Date"]==df["Date"].max()].iloc[0]["LotAnoda"])
# with metric_col[1]:
#     st.metric('Number of Anoda This Year', df[pd.DatetimeIndex(df["Date"]).year==today.year].shape[0])
# with metric_col[2]:
#     st.metric('Latest Actual NAC', round(df[df["Date"]==df["Date"].max()].iloc[0]["NAC Actual"],2))
# st.markdown("###### Select Data Period ")
#
# col1= st.columns(2)
#
# with col1[0]:
#     start_date = st.date_input(
#         "Start date",
#         df["Date"].min().to_pydatetime(),
#         min_value=df["Date"].min().to_pydatetime(),
#         max_value=today,
#     )
#
# with col1[1]:
#     end_date = st.date_input(
#         "End date",
#         today,
#         min_value=df["Date"].min().to_pydatetime(),
#         max_value=today,
#     )
#
## Food Price PLOT ##
st.subheader("Poverty Map")
col1 = st.columns(2)
with col1[0]:
    year = st.selectbox("Select Year", ('2020','2019','2018','2017'))

data_geo = json.load(open('data/countries.geojson'))
data_food_insecurity = pd.read_excel('data/food insecurity.xlsx')
def center():
    address = 'Indonesia'
    geolocator = Nominatim(user_agent="id_explorer")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

def threshold(data):
    threshold_scale = np.linspace(data_food_insecurity[year].min(),
                              data_food_insecurity[year].max(),
                              10, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale

def show_maps(data, threshold_scale):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_food_insecurity,
        columns=['Country Code',year],
        key_on='feature.properties.ISO_A3',
        threshold_scale=threshold_scale,
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Food Insecurity",
        highlight=True,
        reset=True).add_to(world_map)

    folium.LayerControl().add_to(world_map)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['ADMIN'],
                                                        aliases=['ADMIN'],
                                                        labels=True))
    folium_static(world_map)

centers = center()

#select_maps = st.sidebar.selectbox(
#    "What data do you want to see?",
#    ("OpenStreetMap", "Stamen Terrain","Stamen Toner")
#)


world_map = folium.Map(tiles="OpenStreetMap", location=[centers[0], centers[1]], zoom_start=3)

#data_food_insecurity['District'] = data_food_insecurity['District'].str.title()
#data_food_insecurity = data_food_insecurity.replace({'District':'Pabean Cantikan'},'Pabean Cantian')
#data_food_insecurity = data_food_insecurity.replace({'District':'Karangpilang'},'Karang Pilang')

#dicts = {"Total_Pop":'Total Population',
#        "Male_Pop": 'Male Population',
#        "Female_Pop": 'Female Population',
#        "Area_Region": 'Areas Region(km squared)'}

#for idx in range(len(data_geo['features'])):
#    country_code = data_geo['features'][idx]['properties']['ISO_A3']
#    data_geo['features'][idx]['properties']['Food Insecurity'][year] = data_food_insecurity.loc[data_food_insecurity['Country Code']==country_code,str(year)].tolist()[0]

show_maps(year, threshold(year))


#selected_data['Anoda Type'] = selected_data['LotAnoda'].apply(lambda x: x[:3])
# col2 = st.columns(3)
# with col2[0]:
#     nac_option = st.selectbox("Select NAC data type", ("Actual and Calculation", "Actual", "Calculation"))
# filter = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
# selected_data = df.loc[filter]
#
# if nac_option == "Actual and Calculation":
#     selected_data_nac = selected_data.loc[:, ['Date', 'NAC Actual', 'NAC Calc']]
#     selected_data_nac = selected_data_nac.melt('Date', var_name='Type', value_name='NAC')
#     ch = alt.Chart(selected_data_nac).mark_line().encode(
#         x='Date',
#         #y=column_name,
#         y=alt.Y('NAC', scale=alt.Scale(domain=[350, 550])),
#         color='Type',
#         tooltip=[alt.Tooltip('NAC', format=",.2f"), 'Date'],
#     ).interactive()
# else:
#     if nac_option == "Actual":
#         column_name = "NAC Actual"
#     elif nac_option == "Calculation":
#         column_name = "NAC Calc"
#     ch = alt.Chart(selected_data).mark_line().encode(
#         x='Date',
#         # y=column_name,
#         y=alt.Y(column_name, scale=alt.Scale(domain=[350, 550])),
#         tooltip=[alt.Tooltip(column_name, format=",.2f"), 'Date'],
#         ).interactive()
#
# st.altair_chart(ch,use_container_width=True,)
#
#
# ## ANODA TYPE PLOT ##
# st.subheader("Anoda Type by Time")
#
# selected_data['Anoda Type'] = selected_data['LotAnoda'].apply(lambda x: x[:3])
#
# options = st.multiselect(
#     'Select Anoda Type',
#     selected_data['Anoda Type'].unique(),
#     ['MGE', 'WGE'])
#
# selected_data_anoda = selected_data[selected_data['Anoda Type'].isin(options)]
#
#
# st.altair_chart(
#     alt.Chart(selected_data_anoda).mark_bar().encode(
#         x='Date',
#         y='count(Anoda Type)',
#         color='Anoda Type',
#         tooltip=['Anoda Type', 'Date', 'count(Anoda Type)']
#     ).interactive(),use_container_width=True,)
#
#
# col3 = st.columns(3)
#
# ## CPC HS Pie Chart
# st.markdown("###### CPC High Sulfur Distribution")
# cpc_hs = selected_data['CPC HS 1'].value_counts().rename_axis('CPC HS').reset_index(name='Counts')
# start_row = 5
# cpc_hs.iloc[start_row] = cpc_hs.iloc[start_row:].sum()
# cpc_hs = cpc_hs.iloc[:start_row + 1]
# cpc_hs.iloc[-1,0] = "Others"
# sum_cpc_hs=cpc_hs["Counts"].sum()
# cpc_hs["Percentage"] = cpc_hs["Counts"].apply(lambda x: round((x/sum_cpc_hs)*100,2))
#
# st.altair_chart(
#     alt.Chart(cpc_hs).mark_arc().encode(
#     theta=alt.Theta(field="Percentage", type="quantitative"),
#     color=alt.Color(field="CPC HS", type="nominal"),
#     tooltip=['CPC HS', 'Counts', 'Percentage']
# ), use_container_width=True, )
#
#
# ## CPC LS Pie Chart
# st.markdown("###### CPC Low Sulfur Distribution")
# cpc_ls = selected_data['CPC LS 1'].value_counts().rename_axis('CPC LS').reset_index(name='Counts')
# start_row = 5
# cpc_ls.iloc[start_row] = cpc_ls.iloc[start_row:].sum()
# cpc_ls = cpc_ls.iloc[:start_row + 1]
# cpc_ls.iloc[-1,0] = "Others"
# sum_cpc_ls = cpc_ls["Counts"].sum()
# cpc_ls["Percentage"] = cpc_ls["Counts"].apply(lambda x: round((x/sum_cpc_ls)*100,2))
#
# st.altair_chart(
#     alt.Chart(cpc_ls).mark_arc().encode(
#     theta=alt.Theta(field="Percentage", type="quantitative"),
#     color=alt.Color(field="CPC LS", type="nominal"),
#     tooltip=['CPC LS', 'Counts', 'Percentage']
# ), use_container_width=True, )
