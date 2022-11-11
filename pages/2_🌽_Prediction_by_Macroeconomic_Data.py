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
    page_title="Poverty Prediction with Macroeconomic Indicators - Povtrait",
    page_icon=icon,
    layout='wide',
    initial_sidebar_state='collapsed'
)


# Display team's logo
image = Image.open('resources/logo-povtrait small.png')
st.image(image)

# Set title
st.title('Poverty Potrait with Macroeconomic Indicators')

# Load the data
df = pd.read_excel("data/Gas and Food Price.xlsx")
df_country = pd.read_csv("data/master_negara_model2_iso2.csv")
df_template = pd.read_excel("data/template_model2.xlsx")

def predict_poverty(data, country_option):
    # Load the model
    country_code = df_country.loc[df_country["nama_negara_model2"]==country_option,'iso2'].to_list()[0]
    with open('models/model price/'+country_code+'_task2.pkl', 'rb') as f:
        model = pickle.load(f)
    result = model.predict(data)
    return result

energy_tab, food_tab, fertilizer_tab, feature_importance, pred_single_tab, pred_batch_tab  = st.tabs(["Energy Price Statistics", "Food Price Statistics", "Fertilizer Price Statistics", "Poverty Prediction Feature Importance", "Single Poverty Prediction", "Batch Poverty Prediction"])

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

    st.markdown("##### Oils and Meals")
    fats_oil_df = df.iloc[:,20:31]
    st.altair_chart(aly.dist(fats_oil_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(fats_oil_df))

    st.markdown("##### Grains")
    crops_fruits_df = df.loc[:,["Barley", "Maize", "Sorghum", "Rice, Thai 5% ", "Rice, Thai 25% ", "Rice, Viet Namese 5%", "Wheat, US SRW **", "Wheat, US HRW"]]
    st.altair_chart(aly.dist(crops_fruits_df,mark='line'), use_container_width=True,)
    st.altair_chart(aly.corr(crops_fruits_df))

    st.markdown("##### Other Foods")
    others_df = df.iloc[:,40:-5]
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


with feature_importance:
    st.subheader("Poverty Prediction Feature Importance")
    col_fi = st.columns(3)
    with col_fi[0]:
        country_option = st.selectbox("Select Country", sorted(df_country["nama_negara_model2"].unique()), key = "Feature Importance")

    country_code = df_country.loc[df_country["nama_negara_model2"] == country_option, 'iso2'].to_list()[0]
    image = Image.open('resources/feature importance/'+country_code+'.png')
    st.image(image)

###### Tab 4: Single Prediction ######
with pred_single_tab:
    st.subheader("Predicting Poverty with Macroeconomic Indicators")
    col2 = st.columns(3)

    country_option = st.selectbox("Select Country", sorted(df_country["nama_negara_model2"].unique()))
    # Sliders for the variables
    with col2[0]:

        #gdp = st.slider(
        #    'Gross Domestic Product',
        #    0, 50000000000, 20000000)

        gdp = st.text_input('Gross Domestic Product', 20000000)

        beverages = st.slider(
            'Beverages',
            0.0, 500.0, 50.0)

        grains = st.slider(
            'Grains',
            0.0, 500.0, 50.0)

    with col2[1]:
        #ge = st.slider(
        #    'Government Final Consumption Expenditure',
        #    0, 50000000000, 20000000)

        ge = st.text_input('Government Final Consumption Expenditure', 20000000)

        other_food = st.slider(
            'Other Food',
            0.0, 500.0, 50.0)


    with col2[2]:
        energy = st.slider(
            'Energy',
            0.0, 500.0, 50.0)

        oils_meals = st.slider(
            'Oils & Meals',
            0.0, 500.0, 50.0)

        fertilizer = st.slider(
            'Fertilizers',
            0.0, 500.0, 50.0)

    # Create dataframe for the features
    features = {
                'gdp': float(gdp),
                'ge': float(ge),
                'Energy': energy,
                'Beverages': beverages,
                'Oils & Meals': oils_meals,
                'Grains': grains,
                'Other Food': other_food,
                'Fertilizers': fertilizer,
                }
    features_df = pd.DataFrame([features])

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
    st.markdown('#### Upload the macroeconomic indicators data')

    st.write("Please make sure the uploaded file follows the right template.")
    # Create the template file
    template_file = to_excel(df_template)

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
        country_option_batch = st.selectbox("Select Country", sorted(df_country["nama_negara_model2"].unique()), key="Country Option Batch")

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
            file_name='predicted poverty by macroeconomic indicators.xlsx',
        )





