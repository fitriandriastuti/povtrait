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


# Display team's logo
image = Image.open('resources/logo-povtrait small.png')
st.image(image)

# Set title
st.title('Poverty Potrait with Prices Data')

# Load the data
df = pd.read_excel("data/Gas and Food Price.xlsx")
df_country = pd.read_excel("data/country models and score.xlsx")

def predict_poverty(data, country_option):
    # Load the model
    model_path = df_country.loc[df_country["country name"]==country_option,'model name'].to_list()[0]
    with open('models/'+model_path, 'rb') as f:
        model = pickle.load(f)
    result = model.predict(data)
    return result

energy_tab, food_tab, fertilizer_tab, pred_single_tab, pred_batch_tab  = st.tabs(["Energy Price Statistics", "Food Price Statistics", "Fertilizer Price Statistics", "Single Poverty Prediction", "Batch Poverty Prediction"])

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


###### Tab 4: Single Prediction ######
with pred_single_tab:
    st.subheader("Predicting Poverty with Prices")
    col2 = st.columns(3)

    country_option = st.selectbox("Select Country", df_country["country name"].unique())
    # Sliders for the variables
    with col2[0]:
        real_gdp = st.slider(
            'Real GDP',
            0.0, 1.0, 0.5)
        beverages = st.slider(
            'Beverages Price',
            0.0, 1.0, 0.5)

        grains = st.slider(
            'Grains Price',
            0.0, 1.0, 0.5)

    with col2[1]:
        real_gfce = st.slider(
            'Real GFCE',
            0.0, 1.0, 0.5)
        food = st.slider(
            'Food Price',
            0.0, 1.0, 0.5)

        other_food = st.slider(
            'Other Food Price',
            0.0, 1.0, 0.5)


    with col2[2]:
        energy = st.slider(
            'Energy Price',
            0.0, 1.0, 0.5)

        oils_meals = st.slider(
            'Oils & Meals Price',
            0.0, 1.0, 0.5)

        fertilizer = st.slider(
            'Fertilizer Price',
            0.0, 1.0, 0.5)

    # Create dataframe for the features
    features = {
                'Real GDP': real_gdp,
                'Real GFCE': real_gfce,
                'Energy Price': energy,
                'Beverages Price': beverages,
                'Food Price': food,
                'Oils & Meals Price': oils_meals,
                'Grains Price': grains,
                'Other Food Price': other_food,
                'Fertilizer Price': fertilizer,
                }
    features_df = pd.DataFrame([features])

    if st.button('Predict', key="Button Predict Single"):
        prediction = predict_poverty(features_df, country_option)
        # Display the prediction
        st.markdown('#### Predicted Poverty: ' + str(round(prediction[0], 2)))
        #st.markdown('#### Predicted Poverty: ' + str(30))


###### Tab 5: Batch Prediction ######
with pred_batch_tab:
    #@st.cache
    # Function to create an Excel file
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    # Upload the excel file
    st.markdown('#### Upload the prices data')

    st.write("Please make sure the uploaded file follows the right template.")
    # Create the template file
    template_file = to_excel(df.iloc[:,-1:])

    # Button to download the template file
    st.download_button(
        label='📥 Download template file',
        data=template_file,
        file_name='template_prices.xlsx',
    )
    # Input file uploader
    uploaded_file = st.file_uploader("Choose an Excel file")
    # Read the input file
    if uploaded_file is not None:
        df_input = pd.read_excel(uploaded_file)
        st.dataframe(df_input)

    col3 = st.columns(3)

    with col3[0]:
        country_option_batch = st.selectbox("Select Country", df_country["country name"].unique(), key="Country Option Batch")

    # Predict poverty based on the input dataframe
    if st.button('Predict', key="Button Predict Batch"):
        st.markdown('#### Predicted Poverty')
        prediction_batch = predict_poverty(df_input,country_option_batch)

        # Add prediction as a new column
        df_predicted = df_input.assign(Poverty=prediction_batch)

        # Display prediction dataframe
        st.dataframe(df_predicted)

        # Create Excel file to download
        excel_file = to_excel(df_predicted)

        # Button to download the prediction data
        st.download_button(
            label='📥 Download data as Excel',
            data=excel_file,
            file_name='predicted Poverty by prices.xlsx',
        )

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



