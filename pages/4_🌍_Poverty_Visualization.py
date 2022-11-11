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
df = pd.read_excel("data/NTL and Poverty.xlsx")
df['Year'] = df['Year'].astype(str)


# Create multiple tabs
vis_tab, pred_single_tab  = st.tabs(["Map Visualization", "Single Prediction"])

###### Tab 1: Visualisation ######
with vis_tab:
    st.subheader("Visualization")
    col1 = st.columns(2)

    with col1[0]:
        option = st.selectbox("Select Data", ("NTL", "Poverty"))

    st.markdown('#### Poverty and NTL Over the Year')
    st.altair_chart(
            alt.Chart(df).mark_line(color='orange').encode(
                x='Year',
                y=option,
                # y=alt.Y('Value', scale=alt.Scale(domain=[350, 550])),
                tooltip=['Year', alt.Tooltip(option, format=",.2f")],
            ).interactive()
            , use_container_width=True, )

    st.markdown('#### Scatter Plot')
    st.altair_chart(
            alt.Chart(df).mark_circle(size=90,color='steelblue').encode(
                x='NTL',
                y='Poverty',
                tooltip=['Year', 'NTL', 'Poverty']
            ).interactive(),
            use_container_width=True, )




###### Tab 2: Single Prediction with All Variables ######
with pred_single_tab:
    st.subheader("Predicting Poverty with NTL")
    col2 = st.columns(2)

    # Sliders for the variables
    with col2[0]:
        ntl = st.slider(
            'NTL',
            0.0, 1.0, 0.5)


    # # Create dataframe for the features
    # features = {
    #             'NTL': ntl,
    #             }
    # features_df = pd.DataFrame([features])
    #
    #
    # prediction = predict_poverty(features_df)
    #
    # # Display the prediction
    # st.markdown('#### Predicted Poverty: ' + str(round(prediction[0], 2)))
    # #st.markdown('#### Predicted Poverty: ' + str(30))

