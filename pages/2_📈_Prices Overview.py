import streamlit as st
from PIL import Image
import pickle
import numpy as np
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import altair_ally as aly
import altair as alt

## Set page icon
icon = Image.open("./resources/favicon.ico")

## Set page title and layout
st.set_page_config(
    page_title="Poverty Prediction by NTL - Povtrait",
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

# Display team's logo
image = Image.open('resources/logo-povtrait small.png')
st.image(image)

# Set title
st.title('Energy, Food, and Fertilizer Prices Overview')

# Load the data
df = pd.read_excel("data/Gas and Food Price.xlsx")


energy_tab, food_tab, fertilizer_tab  = st.tabs(["Energy Price", "Food Price", "Fertilizer Price"])

with energy_tab:
    st.markdown("### Energy Prices")
    energy_df = df.iloc[:,3:13]
    #st.dataframe(energy_df)
    st.markdown("##### Descriptive Statistics")
    st.dataframe(energy_df.describe())
    st.markdown("##### Distribution")
    st.altair_chart(aly.dist(energy_df,mark='line'), use_container_width=True,)
    st.markdown("##### Correlation")
    st.altair_chart(aly.corr(energy_df))

with food_tab:
    st.markdown("### Food Prices")
    st.markdown("##### Descriptive Statistics")
    food_df = df.iloc[:,13:-4]
    st.dataframe(food_df.describe())

    st.markdown("##### Beverages")
    beverages_df = df.iloc[:,13:20]
    st.altair_chart(aly.dist(beverages_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(beverages_df ))

    st.markdown("##### Fats and Oil")
    fats_oil_df = df.iloc[:,20:31]
    st.altair_chart(aly.dist(fats_oil_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(fats_oil_df))

    st.markdown("##### Crops and Fruits")
    crops_fruits_df = df.iloc[:,31:43]
    st.altair_chart(aly.dist(crops_fruits_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(crops_fruits_df))

    st.markdown("##### Animal Products")
    animal_df = df.iloc[:,43:46]
    st.altair_chart(aly.dist(animal_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(animal_df))

    st.markdown("##### Others")
    others_df = df.iloc[:,46:]
    st.altair_chart(aly.dist(others_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(others_df))

with fertilizer_tab:
    st.markdown("### Fertilizer Prices")
    fertilizer_df = df.iloc[:,-4:]
    #st.dataframe(fertilizer_df)
    st.markdown("##### Descriptive Statistics")
    st.dataframe(fertilizer_df.describe())
    st.markdown("##### Distribution")
    st.altair_chart(aly.dist(fertilizer_df,mark='line'), use_container_width=True,)
    st.markdown("##### Correlation")
    st.altair_chart(aly.corr(fertilizer_df))


# Scatter plot between predictor and target
#st.markdown("#### Relationship between prices and poverty")
#col_vis = st.columns(3)
#with col_vis[0]:
#    column_name = st.selectbox("Select predictor variable", df.columns)

#st.altair_chart(alt.Chart(df).mark_circle(size=60).encode(
#        x='RR CO2',
#        y=column_name,
#        tooltip=['RR CO2', column_name]
#    ).interactive(), use_container_width=True,)



